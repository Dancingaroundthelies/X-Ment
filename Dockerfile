# Use an official lightweight Python image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Command to run the Flask app
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT:-5000} app:app"]
