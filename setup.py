import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="redis-mass-get",
    version="0.0.8",
    description="Queries KEYS from Redis and performans an efficient MGET. Helps with querying your Redis.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/KeesCBakker/redis-mass-get",
    author="Kees C. Bakker / KeesTalksTech",
    author_email="info@keestalkstech.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["redis_mass_get"],
    include_package_data=True,
    install_requires=["redis"],
    entry_points={
        "console_scripts": [
            "redis_mass_get=redis_mass_get.__main__:main",
            "rmg=redis_mass_get.__main__:main",
            "redis-mass-get=redis_mass_get.__main__:main"
        ]
    },
)
