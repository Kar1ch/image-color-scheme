#!/bin/bash

# Проверяем, запущен ли Waybar
if pgrep -x "waybar" > /dev/null; then
    # Убиваем процесс Waybar
    pkill waybar
    # Даем немного времени процессу завершиться
    sleep 1
fi

# Запускаем Waybar снова
waybar &
