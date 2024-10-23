# Use the official Ubuntu image as the base image
FROM ubuntu:latest

# Set the working directory in the container
WORKDIR /txtedit

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    g++ \
    libcpprest-dev \
    libboost-all-dev \
    libssl-dev \
    cmake

# Copy the source code into the container
COPY . .

RUN echo "$PWD"

RUN mkdir build && cd build && cmake .. && make

# Command to run the API when the container starts
CMD ["./build/txtedit"]
