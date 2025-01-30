from setuptools import setup, find_packages

setup(
    name="synternet-pubsub",
    version="0.2",
    py_modules=["helper"],
    packages=find_packages(),
    install_requires=[
        "nats.py==2.9.0",
        "nkeys==0.2.1"
    ],
    description="A helper package for Synternet DL",
    author="Synternet",
    url="https://github.com/Synternet/pubsub-python",
    python_requires='>=3.6',
)
