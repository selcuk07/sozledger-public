from setuptools import setup, find_packages

setup(
    name="soz-ledger",
    version="0.2.0",
    description="Python SDK for Soz Ledger -- AI Agent Trust Protocol",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "httpx>=0.25.0",
    ],
    extras_require={
        "test": ["pytest>=7.0"],
    },
)
