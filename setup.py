import os
from setuptools import setup, find_packages


__version__ = "0.1.2"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

template_files = package_files('catapult/templates')

setup(
    name="catapultt",
    version=f"{__version__}",
    author="Anubhav Tiwari",
    author_email="abt.exp@gmail.com",
    description="A tool for quickly setting up Docker development environments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abtExp/catapult",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "questionary>=1.10.0",
        "rich>=12.0.0",
    ],
    entry_points={
        "console_scripts": [
            "catapultt=catapultt.launch:main",
        ],
    },
    package_data={
        'catapultt': ['config/*.yaml', 'base_images/*.Dockerfile', 'compose_files/*.yaml'] + template_files
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)