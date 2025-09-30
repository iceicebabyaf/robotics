# Используем multi-arch образ ROS2 Humble (Ubuntu 22.04)
FROM ghcr.io/sloretz/ros:humble-desktop

# Устанавливаем Python-инструменты для разработки
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-argcomplete \
    git \
    && rm -rf /var/lib/apt/lists/*

# Создаём рабочую директорию
WORKDIR /ros2_ws

# Инициализация ROS2 (будет подключена при запуске контейнера)
CMD ["bash"]
