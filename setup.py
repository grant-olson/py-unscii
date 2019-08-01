import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unscii",
    version="0.1.0",
    author="Grant T. Olson",
    author_email="kgo@grant-olson.net",
    description="Python Interface for UNSCII bitmapped fonts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/grant-olson/py-unscii",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
