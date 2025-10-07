import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from action_cleaning_robot_interfaces.action import CleaningTask

class CleaningRobotClient(Node):
    def __init__(self):
        super().__init__('cleaning_action_client')
        self.action_client = ActionClient(self, CleaningTask, 'cleaning_task')
        self.task_queue = []
        self.active_task = None

    def dispatch_tasks(self, *tasks):
        """Отправка списка задач для последовательного выполнения."""
        self.task_queue = list(tasks)
        if not self.task_queue:
            self.get_logger().error('Список задач пуст!')
            return
        self.action_client.wait_for_server(timeout_sec=10.0)
        self.process_next_task()

    def process_next_task(self):
        """Обработка следующей задачи из очереди."""
        if not self.task_queue:
            self.get_logger().info('Все задачи выполнены!')
            rclpy.shutdown()
            return

        task = self.task_queue.pop(0)
        task_type, area_size, target_x, target_y = task
        self.active_task = task_type

        goal_msg = CleaningTask.Goal()
        goal_msg.task_type = task_type
        goal_msg.area_size = float(area_size)
        goal_msg.target_x = float(target_x)
        goal_msg.target_y = float(target_y)

        self.get_logger().info(f'Отправка цели: {task_type}')
        send_future = self.action_client.send_goal_async(goal_msg, feedback_callback=self.on_feedback)
        send_future.add_done_callback(self.on_goal_response)

    def on_goal_response(self, future):
        """Обработка ответа на отправленную цель."""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().warning(f'Цель "{self.active_task}" отклонена!')
            self.process_next_task()
            return

        self.get_logger().info(f'Цель "{self.active_task}" принята.')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.on_result)

    def on_result(self, future):
        """Обработка результата выполнения цели."""
        result = future.result().result
        self.get_logger().info(f'Результат для "{self.active_task}": успех={result.success}, точек={result.cleaned_points}, расстояние={result.total_distance:.2f}')
        self.process_next_task()

    def on_feedback(self, feedback_msg):
        """Обработка feedback от сервера."""
        feedback = feedback_msg.feedback
        self.get_logger().info(f'Feedback [{self.active_task}]: прогресс={feedback.progress_percent}%, точек={feedback.current_cleaned_points}, позиция=({feedback.current_x:.2f}, {feedback.current_y:.2f})')

def main(args=None):
    try:
        rclpy.init(args=args)
        client = CleaningRobotClient()
        client.dispatch_tasks(
            ('clean_square', 3.0, 0.0, 0.0),
            ('return_home', 0.0, 5.5, 5.5)
        )
        rclpy.spin(client)
    except Exception as e:
        client.get_logger().error(f'Ошибка: {str(e)}')
    finally:
        client.get_logger().info('Завершение работы клиента')
        rclpy.shutdown()

if __name__ == '__main__':
    main()