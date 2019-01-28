import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="openpay-python",
    version="0.3.4",
    author="openpay",
    install_requires=[
        'lxml',
        'requests==2.20.1'],
    author_email="sam91v@gmail.com",
    description="openpay python sdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/openpaygithub/PythonSDK",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
