import os
import setuptools
from setuptools import setup, find_packages

current_folder = os.path.dirname(os.path.realpath(__file__))
requirements_path = current_folder + "/requirements.txt"

install_requires = []
if os.path.isfile(requirements_path):
    with open(requirements_path) as file:
        install_requires = file.read().splitlines()

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name="neural_style_transfer",
    version="0.0.1",
    author="David Engelmann",
    author_email="david.engelmann44@gmail.com",
    description="Neural Style Transfer with PyTorch and VGG19",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/david-engelmann/neural_style_transfer",
    project_urls={
        "Bug Tracker": "https://github.com/david-engelmann/neural_style_transfer/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,
    python_requires=">=3.6"
)