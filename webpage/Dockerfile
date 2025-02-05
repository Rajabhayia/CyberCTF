# Base image for Python
FROM python:3.12-slim

# Set work directory in container
WORKDIR /app

# Install dependencies
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Copy the backend code into the container
COPY ./webpage/backend /app/

# Expose port 8000 for Django
EXPOSE 8000

# Command to run Django
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
