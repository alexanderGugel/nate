import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nate",
    version="0.0.7",
    author="Alexander Gugel",
    author_email="alexander.gugel@gmail.com",
    description="Make generating HTML fun.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexanderGugel/nate",
    package_data={"nate": ["py.typed"]},
    packages=setuptools.find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
