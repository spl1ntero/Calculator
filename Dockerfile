# Используем базовый образ Python
FROM python:3.12

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем необходимые файлы из хоста внутрь контейнера
COPY templates ./templates
COPY static ./static
COPY feedback.json /app/feedback.json
COPY requirements.txt .
COPY app.py .

# Устанавливаем зависимости Python
RUN pip install -r requirements.txt

# Устанавливаем переменную окружения FLASK_APP
ENV FLASK_APP=app.py

# Запускаем Flask приложение при старте контейнера
CMD ["flask", "run", "--host=0.0.0.0", "--debug"]
