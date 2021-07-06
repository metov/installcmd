from pathlib import Path

import setuptools

setuptools.setup(
    name="installcmd",
    version="0.4.1",
    author="Azat Akhmetov",
    description="Print correct command for installing a package.",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/metov/installcmd",
    packages=setuptools.find_packages(),
    package_data={"": ["commands.yaml"]},
    entry_points={"console_scripts": ["installcmd = installcmd.cli:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "coloredlogs",
        "docopt",
        "python-dotenv",
        "pyyaml",
    ],
)
