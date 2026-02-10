from setuptools import setup, find_packages

setup(
    name="soz-ledger-langchain",
    version="0.1.0",
    description="Soz Ledger integration for LangChain -- automatic promise tracking for tool calls",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "soz-ledger>=0.2.0",
        "langchain-core>=0.2.0",
    ],
    extras_require={
        "test": ["pytest>=7.0"],
    },
)
