# Use an official Ubuntu base image
FROM ubuntu:20.04

# Set environment variables to avoid user prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    nano \
    vim \
    curl \
    wget \
    build-essential \
    git \
    ca-certificates \
    libreadline-dev \
    libncurses-dev \
    libssl-dev \
    libffi-dev \
    libsqlite3-dev \
    zlib1g-dev \
    && apt-get clean
    pip install flask-socketio
    pip install --upgrade pip

# Install EPICS Base
RUN git clone --depth=1 https://github.com/epics-base/epics-base.git /epics/base && \
    cd /epics/base && \
    make

# Set environment variables for EPICS
ENV EPICS_BASE=/epics/base
ENV PATH=$PATH:$EPICS_BASE/bin/linux-x86_64
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$EPICS_BASE/lib/linux-x86_64

# Copy application files
COPY . /app
WORKDIR /app

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Expose port
EXPOSE 5000

# Start application
CMD ["python3", "app.py"]
