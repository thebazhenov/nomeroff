# Используем официальный образ Python 3.9
FROM python:3.9-slim-bullseye

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /

# Установка git
RUN apt-get update && apt-get install -y \
    git \
    libglib2.0-0 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл requirements.txt в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект внутрь контейнера
COPY . .

# Указываем команду запуска вашего скрипта
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8182"]
