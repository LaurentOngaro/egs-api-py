import setuptools
import sys

if sys.version_info < (3, 11):
    sys.exit('python 3.10 or higher is required for this project')

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="egs-api",
    version="0.9.1",
    author="Laurent Ongaro",
    author_email="laurent@gameamea.com",
    description="A minimal asynchronous interface to Epic Games Store in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License", "Operating System :: OS Independent", ],
    python_requires='>=3.11',
)
