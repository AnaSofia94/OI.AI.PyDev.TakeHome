# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container to /app
WORKDIR /app

# Install FFmpeg (this line is new) and some dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Copy Pipfile and Pipfile.lock first to leverage Docker's caching
COPY Pipfile Pipfile.lock /app/

# Install pipenv and project dependencies
RUN pip install pipenv
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of the application code
COPY . /app

# Set PYTHONPATH to include the /app/src directory
ENV PYTHONPATH=/app/src

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["pipenv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]