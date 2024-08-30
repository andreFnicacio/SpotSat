# Dockerfile

# Base image
FROM python:3.11-slim

# Install dependencies for GDAL
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    python3-gdal

# Set environment variables for GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
ENV GDAL_LIBRARY_PATH=/usr/lib/libgdal.so

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Copy the wait-for-it script
COPY wait-for-it.sh /wait-for-it.sh

# Ensure the init_db.py script is executable
RUN chmod +x /app/init_db.py /wait-for-it.sh

# Run the database initialization script, migrate the database, and start the server
CMD ["sh", "-c", "python init_db.py && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
