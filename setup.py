from setuptools import setup, find_packages

setup(
    name="bulk",
    version="0.0.5",
    packages=find_packages(),
    install_requires=["typer>=0.4.1", "bokeh>=2.4.3", "pandas>=1.0.0"],
    extras_require={
        "dev": ["pytest-playwright==0.3.0"],
    },
    entry_points={
        'console_scripts': [
            'bulk = bulk.__main__:app',
        ],
    },
)
