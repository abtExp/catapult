# Docker Development Launcher

A command-line tool to quickly set up and launch Docker-based development environments for various types of projects.

## Features

- Quick setup for C++, Node.js, Python, and Deep Learning projects
- Custom project naming
- Directory selection for project creation
- Automatic Docker image building
- Live code synchronization for development
- Launcher script generation

## Installation

### From PyPI (Recommended)

```bash
pip install docker-dev-launcher
```

### From Source

1. Clone the repository
2. Navigate to the project directory
3. Run:

```bash
pip install -e .
```

## Usage

After installation, you can run the tool with:

```bash
docker-dev
```

Follow the interactive prompts to set up your development environment.

## Requirements

- Python 3.7+
- Docker
- Docker Compose

## Environments Supported

- **C++ Development**: Alpine-based minimal container with CMake
- **Node.js Development**: Node.js with npm and hot reloading
- **Python Development**: Python with pip package management
- **Deep Learning Development**: PyTorch with CUDA support

## License

MIT