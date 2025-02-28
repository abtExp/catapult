from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="catapult",
    version="0.1.0",
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
            "catapult=catapult.launch:main",
        ],
    },
    package_data={
        'catapult/config': ['*.yaml'],
        'catapult/base_images': ['*.Dockerfile'],
        'catapult/compose_files' : ['*.yaml'],
        'catapult/templates' : ['*.*']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)