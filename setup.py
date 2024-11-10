from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="clipboard-share",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for sharing clipboards between computers on a local network",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/clipboard-share",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pyyaml",
        "pyperclip",
        "cryptography",
    ],
    entry_points={
        'console_scripts': [
            'clipboard-server=server:ClipboardServer.start',
            'clipboard-client=client:ClipboardClient.connect',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['config/*.yml'],
    },
) 