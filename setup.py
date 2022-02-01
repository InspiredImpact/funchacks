import setuptools


def long_description() -> str:
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()


setuptools.setup(
    name="funchacks",
    version="1.0.1",
    keywords=[
        "FUNCTIONAL PROGRAMMING",
        "FUNCTION TOOLS",
        "FUNCTION UTILS",
        "UTILS",
    ],
    author="DenyS",
    description="",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    license="Apache License, Version 2.0",
    packages=setuptools.find_namespace_packages(include=["funchacks*"]),
    url="https://github.com/Animatea/funchacks",
    download_url="https://github.com/Animatea/funchacks/archive/refs/heads/main.zip",
    project_urls={
        "GitHub": "https://github.com/Animatea/funchacks",
        "Bug Tracker": "https://github.com/Animatea/funchacks/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Other Audience",
        "Typing :: Typed",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
)
