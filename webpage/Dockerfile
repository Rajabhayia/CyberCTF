# Step 1: Use an official Python image as the base image
FROM python:3.12-slim as base

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Install pipenv to manage dependencies
RUN pip install pipenv

# Step 4: Copy Pipfile and Pipfile.lock from the Webpage directory into the container
COPY Webpage/Pipfile Webpage/Pipfile.lock /app/

# Step 5: Install dependencies inside the container
RUN pipenv install --deploy --ignore-pipfile

# Step 6: Copy the rest of the backend application code into the container
COPY Webpage/backend /app/backend

# Step 7: Expose port 8000 for the Django backend
EXPOSE 8000

# Step 8: Set environment variables for Django settings (optional, replace with your settings)
ENV DJANGO_SETTINGS_MODULE=your_project_name.settings

# Step 9: Run Django's development server (you can replace with Gunicorn or another WSGI server for production)
CMD ["pipenv", "run", "python", "backend/manage.py", "runserver", "0.0.0.0:8000"]
