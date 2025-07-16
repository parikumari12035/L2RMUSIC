# Use a Python and Node.js base image
FROM nikolaik/python-nodejs:python3.10-nodejs19

# Update apt sources to point to the Debian archive (for buster)
RUN sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list && \
    sed -i 's|http://deb.debian.org/debian-security|http://archive.debian.org/debian-security|g' /etc/apt/sources.list && \
    apt-get update --allow-unauthenticated && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the application files into the container
COPY . /app/

# Set the working directory
WORKDIR /app/

# Install Python dependencies from the requirements.txt
RUN pip3 install --no-cache-dir -U -r requirements.txt

# Run the bash start script when the container starts
CMD ["bash", "start"]
