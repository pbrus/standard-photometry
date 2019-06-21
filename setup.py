import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sphot",
    version=__import__("sphot").__version__,
    author="Przemysław Bruś",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pbrus/standard-photometry",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=["pandas", "matplotlib"],
    tests_require=["pytest"],
    keywords=["standard", "photometry", "stars", "brightness"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Utilities",
    ],
)
