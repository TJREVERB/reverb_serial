from setuptools import setup, find_packages

with open("README.rst", "r") as f:
    long_description = f.read()


setup(
    name="reverb_serial",
    version="2.0.1",
    license="GPL",
    packages=find_packages(),
    author="tjreverb",
    author_email="tjreverb@gmail.com",
    description="A fake serial library for testing purposes",
    long_description=long_description,
    url="https://github.com/TJREVERB/reverb_serial",
    python_requires='>=3.6',
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Other Audience",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
    ],
)
