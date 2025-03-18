FROM python:3.10

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the correct port
EXPOSE 8000

# Start the application
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "gemini_app:app"] 