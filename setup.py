from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()


setup(
    name="fasttyper",
    version="2.4.1",
    author="Piotr Domanski",
    author_email="pi.domanski@gmail.com",
    description="Minimalistic typing exercise",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ickyicky/fasttyper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "fasttyper=fasttyper.runner:runner",
        ]
    },
)
