from setuptools import setup, find_packages
import codecs
import os.path


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    # Getting version number without package import:
    # https://packaging.python.org/guides/single-sourcing-package-version/
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='gridsim',
    version=get_version(os.path.join("gridsim", "__init__.py")),
    description='Simple grid-based robot simulator',
    long_description=readme,
    long_description_content_type='text/x-rst',
    python_requires='>=3.6',
    author='Julia Ebert',
    author_email='julia@juliaebert.com',
    url='https://gridsim.readthedocs.io',
    download_url='https://github.com/jtebert/gridsim',
    packages=find_packages(exclude=('tests', 'docs')),
    # license=license,
    install_requires=[
        # List of dependencies
        "pygame",
        "numpy",
        "h5py",
        "pyyaml",
        'pillow',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Framework :: Robot Framework",
        "Development Status :: 3 - Alpha"
    ],
    zip_safe=False,
)
