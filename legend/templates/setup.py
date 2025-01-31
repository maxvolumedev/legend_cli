from setuptools import setup, find_packages

setup(
    name="{{ app_name }}",
    version="0.1.0",
    description="Azure Functions App",
    packages=find_packages(),
    install_requires=[
        "azure-functions>=1.17.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "jinja2>=3.1.2",
        ],
    },
    python_requires=">=3.9",
)
