from setuptools import setup, find_packages

setup(
    name="voltage_divider",
    version="0.2.0",
    description="A Python library to simplify the calculations necessary for adding a voltage divider to your circuit.",
    url="https://github.com/alyssadev/voltagedivider",
    author="Alyssa Smith",
    author_email="alyssa.dev.smith@gmail.com",
    license="MIT",
    extras_requires={
        "schemdraw": [
            "schemdraw"
        ]
    },
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License'
    ]
)
