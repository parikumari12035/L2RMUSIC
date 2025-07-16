FROM nikolaik/python-nodejs:python3.10-nodejs19

# Install necessary dependencies (ffmpeg)
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code into the container
COPY . /app/
WORKDIR /app/

# Install Python dependencies from requirements.txt
RUN pip3 install --no-cache-dir -U -r requirements.txt

# Make the start.sh script executable (if it's a shell script)
RUN chmod +x start.sh  # Ensure this file exists and is executable

# Set the default command to execute your script or entrypoint
CMD ["bash", "start.sh"]  # Modify the filename as needed (if it's start.sh or another file)
