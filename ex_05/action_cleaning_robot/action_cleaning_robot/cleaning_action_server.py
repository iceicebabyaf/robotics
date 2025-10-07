import math
import time
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtlesim.srv import SetPen
from action_cleaning_robot_interfaces.action import CleaningTask

def normalize_angle(angle):
    """Нормализация угла в диапазон [-π, π]."""
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle
# твист - линейная и угловая скорость
"""
NODE#1  cleaning_action_server
"""
class CleaningRobotServer(Node):
    def __init__(self):
        super().__init__('cleaning_action_server')
        self._action_server = ActionServer(
            self,
            CleaningTask,
            'cleaning_task',
            self.handle_goal)
        self.cmd_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pen_client = self.create_client(SetPen, '/turtle1/set_pen')
        while not self.pen_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Ожидание сервиса /turtle1/set_pen...')
        self.set_pen(r=0, g=255, b=0, width=10, off=0) 
        initial_pose = self.fetch_pose()
        self.start_x = initial_pose.x
        self.start_y = initial_pose.y
        self.points_cleaned = set()

    def set_pen(self, r=0, g=0, b=0, width=10, off=0):
        """Настройка пера черепахи."""
        req = SetPen.Request()
        req.r = r
        req.g = g
        req.b = b
        req.width = width
        req.off = off
        self.pen_client.call_async(req)

    """
    подписка на позу черепахи:
    x, y, thetta (нужно нормировать от -пи до пи)
    """
    def fetch_pose(self):
        future = rclpy.task.Future()
        sub = self.create_subscription(
            Pose, '/turtle1/pose',
            lambda msg: future.set_result(msg), 1)
        rclpy.spin_until_future_complete(self, future)
        self.destroy_subscription(sub)
        return future.result()

# goal han
    def handle_goal(self, goal_handle):
        self.get_logger().info(f'Получена цель: {goal_handle.request.task_type}')
        task_type = goal_handle.request.task_type
        feedback_msg = CleaningTask.Feedback()
        result = CleaningTask.Result()

        if task_type == 'clean_square':
            self.get_logger().info('Запуск очистки квадратной области')
            result = self.clean_square(goal_handle.request.area_size, goal_handle)
        elif task_type == 'return_home':
            self.get_logger().info('Запуск возвращения домой')
            result = self.navigate_home(goal_handle.request.target_x, goal_handle.request.target_y, goal_handle)
        else:
            self.get_logger().error(f'Неизвестный тип задачи: {task_type}')
            goal_handle.abort()
            result.success = False
            return result

        if result.success:
            goal_handle.succeed()
        else:
            goal_handle.abort()
        return result

    def clean_square(self, size, goal_handle):
        """Очистка квадратной области горизонтальными полосками."""
        self.get_logger().info(f'Очистка квадратной области размером {size} м')
        cmd = Twist()
        feedback_msg = CleaningTask.Feedback()
        result = CleaningTask.Result()
        feedback_msg.current_cleaned_points = 0
        linear_speed = 1.0 # m/sec
        angular_speed = 1.0 # rad/sec
        # размер клетки
        grid_step = 0.2
        step_size = 0.2
        total_area = size * size
        self.points_cleaned.clear()

        pose = self.fetch_pose() # наклон (таргет)
        center_x, center_y = pose.x, pose.y
        y_top = center_y + size / 2  # верхняя граница
        y_bottom = center_y - size / 2  # нижняя граница
        x_left = center_x - size / 2
        x_right = center_x + size / 2
        current_y = y_top
        direction_right = True  # Начать движение вправо

        while current_y >= y_bottom and rclpy.ok():
            pose = self.fetch_pose()

            # Определение целевой x-координаты
            target_x = x_right if direction_right else x_left
            angle_to_target = math.atan2(current_y - pose.y, target_x - pose.x) # угол к точке target_x (лево/право), current_y(в начале верхняя точка)
            # если 
            angle_diff = normalize_angle(angle_to_target - pose.theta)

            # ЕСЛИ РАЗНИЦА > 0.1 РАДИАН : ПОВОРАЧИВАЕТ. ЕСЛИ НЕТ -> ДВИЖЕТСЯ КАК ДВИГАЛСЯ (МЕЖДУ pose и target)
            if abs(angle_diff) > 0.1:
                cmd.angular.z = angular_speed if angle_diff > 0 else -angular_speed
                cmd.linear.x = 0.0
            else:
                cmd.angular.z = 0.0
                cmd.linear.x = linear_speed

            # отправляет команду скорости в /turtle1/cmd_vel
            self.cmd_publisher.publish(cmd)
            rclpy.spin_once(self, timeout_sec=0.05)

            # Обновление feedback
            feedback_msg.current_x = pose.x
            feedback_msg.current_y = pose.y
            progress = (y_top - pose.y) / size if size > 0 else 0
            feedback_msg.progress_percent = min(100, max(0, int(progress * 100)))
            feedback_msg.current_cleaned_points += 1

            x_cell = round(pose.x / grid_step)
            y_cell = round(pose.y / grid_step)
            self.points_cleaned.add((x_cell, y_cell)) # сохраняет закрашенную клеку

            goal_handle.publish_feedback(feedback_msg) # x, y, %, точки

            # Проверка достижения края полоски
            dist_to_target = abs(pose.x - target_x)
            if dist_to_target < 0.1:
                direction_right = not direction_right
                current_y -= step_size  # Переход к следующей полоске
                # Установить угол для следующей полоски
                target_angle = 0.0 if direction_right else math.pi
                angle_diff = normalize_angle(target_angle - pose.theta)
                while abs(angle_diff) > 0.1 and rclpy.ok():
                    cmd.angular.z = angular_speed if angle_diff > 0 else -angular_speed
                    cmd.linear.x = 0.0
                    self.cmd_publisher.publish(cmd)
                    rclpy.spin_once(self, timeout_sec=0.05)
                    pose = self.fetch_pose()
                    angle_diff = normalize_angle(target_angle - pose.theta)

            if goal_handle.is_cancel_requested:
                self.get_logger().info('Очистка области отменена')
                cmd.linear.x = 0.0
                cmd.angular.z = 0.0
                self.cmd_publisher.publish(cmd)
                result.success = False
                return result

        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
        self.cmd_publisher.publish(cmd)
        result.success = True
        result.cleaned_points = len(self.points_cleaned)
        result.total_distance = total_area
        self.get_logger().info(f'Очистка завершена: точек={result.cleaned_points}, расстояние={result.total_distance:.2f}')
        return result
    """
    RETURN HOME
    """
    def navigate_home(self, target_x, target_y, goal_handle):
    
        self.get_logger().info(f'Возврат в ({target_x}, {target_y})')
        feedback_msg = CleaningTask.Feedback()
        result = CleaningTask.Result()
        feedback_msg.current_cleaned_points = 0
        pose = self.fetch_pose()
        distance = math.sqrt((target_x - pose.x)**2 + (target_y - pose.y)**2)

        while True:
            pose = self.fetch_pose()
            angle_to_target = math.atan2(target_y - pose.y, target_x - pose.x)
            angle_diff = normalize_angle(angle_to_target - pose.theta)
            current_distance = math.sqrt((target_x - pose.x)**2 + (target_y - pose.y)**2)

            cmd = Twist()
            if abs(angle_diff) > 0.1:
                cmd.angular.z = 1.0 if angle_diff > 0 else -1.0  # Увеличенная угловая скорость
                cmd.linear.x = 0.0
            elif current_distance > 0.1:
                cmd.angular.z = 0.0
                cmd.linear.x = 1.0  # Увеличенная линейная скорость
            else:
                cmd.angular.z = 0.0
                cmd.linear.x = 0.0
                self.cmd_publisher.publish(cmd)
                break

            feedback_msg.current_x = pose.x
            feedback_msg.current_y = pose.y
            feedback_msg.progress_percent = max(0, 100 - int(current_distance / distance * 100))
            goal_handle.publish_feedback(feedback_msg)
            self.cmd_publisher.publish(cmd)
            rclpy.spin_once(self, timeout_sec=0.05)

        result.success = True
        result.cleaned_points = 0
        result.total_distance = distance
        self.get_logger().info(f'Возврат домой завершен: расстояние={result.total_distance:.2f}')
        return result

def main(args=None):
    rclpy.init(args=args)
    server = CleaningRobotServer()
    rclpy.spin(server)
    rclpy.shutdown()

if __name__ == '__main__':
    main()