# Use Alpine as a much smaller base image
FROM alpine:3.18 as builder

# Set the working directory
WORKDIR /code

# Install minimal build dependencies
RUN apk add --no-cache &&
    g++ \\
    cmake \\
    make \\
    boost-dev \\
    openssl-dev

# Copy only the files needed for cmake first to take advantage of Docker's layer caching
COPY CMakeLists.txt ./
COPY src/ ./src/

# Create build directory and build
RUN mkdir -p build && \\
    cd build && \\
    cmake .. && \\
    make -j$(nproc)

# Use a smaller runtime image
FROM alpine:3.18

# Install only runtime dependencies
RUN apk add --no-cache \\
    libstdc++ \\
    boost \\
    openssl

WORKDIR /app

# Copy only the built application from the builder stage
COPY --from=builder /code/build/code .

# Set the entry point to run the application
CMD ["./code"]