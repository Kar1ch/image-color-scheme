# Создаём окружение
python -m venv venv

# Активируем
source venv/bin/activate.fish

# Устанавливаем пакет
pip install numpy

# Проверяем, что всё работает
python -c "import numpy; print(numpy.__version__)"

# Выходим
deactivate
