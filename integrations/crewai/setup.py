from setuptools import setup, find_packages

setup(
    name="soz-ledger-crewai",
    version="0.1.0",
    description="Soz Ledger integration for CrewAI -- automatic promise tracking for completed tasks",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "soz-ledger>=0.2.0",
        "crewai>=0.80.0",
    ],
    extras_require={
        "test": ["pytest>=7.0"],
    },
)
