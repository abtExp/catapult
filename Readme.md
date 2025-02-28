# Catapultt Docker Development

[![PyPI version](https://img.shields.io/pypi/v/catapultt.svg)](https://pypi.org/project/catapultt/)
[![Python Versions](https://img.shields.io/pypi/pyversions/catapultt.svg)](https://pypi.org/project/catapultt/)
[![License](https://img.shields.io/pypi/l/catapultt.svg)](https://github.com/abtExp/catapult/blob/main/LICENSE)

A streamlined tool for quickly setting up Docker development environments for various project types.

## Features

- **Multiple Environment Types**: Support for C++, Node.js, Python, and Deep Learning projects
- **Minimal Configuration**: Optimized Docker configurations with only the essentials
- **Live Development**: Automatic code synchronization and rebuilding
- **Project Customization**: Custom naming and file structure for your projects
- **Consistent Workflow**: Same development experience across different technologies

## Installation

```bash
pip install catapultt
```

### Requirements

- Python 3.7+
- Docker
- Docker Compose

## Quick Start

```bash
# Launch the interactive tool
catapultt

# Select environment type, project name, and location
# Follow the prompts and you're ready to code!
```

## Environment Types

### C++ Development
- Alpine-based minimal container
- CMake configuration
- Live rebuild on code changes

### Node.js Development
- Node Alpine image
- Automatic npm dependency management
- Fast file syncing for source files

### Python Development
- Python slim image
- Requirements.txt integration
- Fast file syncing

### Deep Learning Development
- NVIDIA PyTorch image with CUDA support
- GPU acceleration support
- Pre-configured with common data science libraries

## Examples

### Creating a New Python Project

```bash
$ catapultt

# Select "Python Development"
# Name your project "my-python-app"
# Choose project location
# Launch the environment
```

### Working with a Project

After setup, your project directory will contain:
- Dockerfile and docker-compose.yml
- Initial template files for your chosen environment
- A launch script for easy startup

## Customization

You can customize templates by editing files in:
```
~/.catapultt/templates/
```

Configuration options are available in:
```
~/.catapultt/templates.yaml
```

## License

MIT License - see the [LICENSE](https://github.com/abtExp/catapult/blob/main/LICENSE) file for details.