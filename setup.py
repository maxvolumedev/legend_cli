from setuptools import setup, find_packages
import os

# Read version from _version.py
version = {}
with open(os.path.join("legend", "_version.py")) as f:
    exec(f.read(), version)

setup(
    name="legend-cli",
    version=version["__version__"],
    description="A CLI for managing Azure Functions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "jinja2>=3.1.2",
        "azure-functions",
        "tomli>=2.0.1",  # For reading TOML configuration files
    ],
    entry_points={
        "console_scripts": [
            "legend=legend.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Operating System :: MacOS :: MacOS X",  # Added since we only support macOS for now
    ],
    python_requires=">=3.9",
    options={
        "bdist_wheel": {
            "universal": True
        }
    }
)
