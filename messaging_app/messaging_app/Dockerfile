FROM python:3.10.0

# Set the working directory
WORKDIR /app

RUN pip install --no-cache-dir requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

ENV DJANGO_SETTINGS_MODULE=app.settings



EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
