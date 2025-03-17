FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY task_management_system .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]