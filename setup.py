from setuptools import setup, find_packages

setup(
    name="legend-cli",
    version="0.1.0",
    description="A CLI for managing Azure Functions, inspired by Ruby on Rails",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "jinja2>=3.1.2",
        "azure-functions-core-tools>=4.0.5611",
    ],
    entry_points={
        "console_scripts": [
            "legend=legend.legend:main",
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
    ],
    python_requires=">=3.9",
)
