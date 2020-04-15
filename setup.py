from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='gridsim',
    version='0.1.1',
    description='Simple grid-based robot simulator',
    long_description=readme,
    long_description_content_type='text/markdown',
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
        "h5py"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Framework :: Robot Framework",
        "Development Status :: 3 - Alpha"
    ],
    zip_safe=False,
)
