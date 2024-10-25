from setuptools import setup, find_packages

setup(
    name="synternet-pubsub",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "nats.py==2.9.0",
        "nkeys==0.1.0"
    ],
    description="A helper package for Synternet DL",
    author="Synternet",
    url="https://github.com/Synternet/pubsub-python",
    python_requires='>=3.6',
)
