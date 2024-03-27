# Base Image (Choose a suitable Python version)
FROM python:3.12-slim

# Work Directory
WORKDIR /app

# Install Dependencies and Create Virtual Environment
COPY Pipfile ./

# Install Pipenv
RUN pip install pipenv

# Install Dependencies
RUN pipenv install --deploy

# Copy Bot Code
COPY . ./

# Background Execution (Assuming you're using a task scheduler or supervisor within your bot code)
CMD ["pipenv", "run", "python", "main.py"]
