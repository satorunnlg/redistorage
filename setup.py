from setuptools import setup, find_packages

setup(
    name="redistorage",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["redis"],
    python_requires=">=3.7",
    author="Kazuki Shioda",
    author_email="satorunnlg@gmail.com",
    description="A Redis-based persistent model class for Python",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/satorunnlg/redistorage.git",  # GitHub URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
