import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="installcmd-metov",
    version="0.1.1",
    author="Azat Akhmetov",
    description="Print correct command for installing a package.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/metov/installcmd",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["installcmd = installcmd.cli:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["pyyaml", "docopt"],
)
