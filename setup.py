from setuptools import find_packages, setup

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name='lenny_intensifies',
    version='0.1.0',
    author='David Buckley',
    author_email='david@davidbuckley.ca',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pillow',
        'numpy',
        'scipy',
        'typer'
    ],
    entry_points = {
        'console_scripts': [
            'lenny-gen=lenny_intensifies.cli:app'
        ]
    }
)
