#!/usr/bin/env python3
"""
Setup script for NL-to-Task-Trace package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="nl-to-task-trace",
    version="0.1.0",
    author="NL-to-Task-Trace Team",
    author_email="contact@example.com",
    description="A system for converting natural language descriptions to structured task traces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tingli98/NL-to-Task-Trace",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
        ]
    },
    entry_points={
        "console_scripts": [
            "nl-to-task-trace=cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)