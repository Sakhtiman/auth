# Use the official Python image as a base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirement.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Copy the entire local directory into the container at /app
COPY . .

# Set the environment variable for the SQLite database URL
ENV SQLALCHEMY_DATABASE_URL="sqlite:///mydatabase/user.db"

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

