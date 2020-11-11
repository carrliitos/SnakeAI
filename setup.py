from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
	name="SnakeAI-pkg-Carrliitos",
	version="0.0.1",
	author="Benzon Carlitos Salazar",
	description="A SnakeAI package",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/carrliitos/SnakeAI",
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
	packages=find_packages('snake'),
	package_dir={'': 'snake'},
)