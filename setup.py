from setuptools import setup, find_packages

setup(
    name="bulk",
    version="0.4.0",
    packages=find_packages(),
    install_requires=["radicli>=0.0.8,<0.1.0", "bokeh>=2.4.3,<3.0.0", "pandas>=1.0.0", "wasabi>=0.9.1", "numpy<2", "jupyter-scatter", "scikit-learn"],
    extras_require={
        "dev": ["pytest-playwright==0.3.0"],
    },
    entry_points={
        'console_scripts': [
            'bulk = bulk.__main__:app',
        ],
    },
)
