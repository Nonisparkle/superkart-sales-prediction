FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the backend application, dependencies, and serialized model
COPY . .

# Install dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask API port
EXPOSE 7860

# Start the Flask application using Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:superkart_api"]
