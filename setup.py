from setuptools import setup, find_packages
import re
from pathlib import Path

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from __init__.py
def get_version():
    init_file = Path(__file__).parent / "easyscript" / "__init__.py"
    content = init_file.read_text(encoding='utf-8')
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        raise RuntimeError("Unable to find version string in __init__.py")
    return match.group(1)

setup(
    name="easyscript",
    version=get_version(),
    author="EasyScript",
    author_email="java4life@gmail.com",
    description="A simple scripting language that blends Python and JavaScript syntax",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rhulha/easyscript",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies
    ],
    entry_points={
        'console_scripts': [
            'easyscript=easyscript.__main__:main',
        ],
    },
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black",
            "flake8",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/rhulha/easyscript/issues",
        "Source": "https://github.com/rhulha/easyscript",
        "Documentation": "https://github.com/rhulha/easyscript#readme",
    },
)