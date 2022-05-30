from setuptools import setup, find_packages

setup(
    name="bulk",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'bulk = bulk.__main__:app',
        ],
    },
)