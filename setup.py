from setuptools import setup, find_packages

setup(
    name='cadscript',
    description="A Python module for creating 3D models with scripts.",
    long_description="A Python module for creating 3D models with scripts.",
    version='0.4.0',
    url="https://github.com/cadscriptHQ/cadscript",
    license="Apache Public License 2.0",
    author='Andreas Kahler',
    author_email='mail@andreaskahler.com',
    packages=find_packages(),
    install_requires=[
        'cadquery'
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
    ]
)
