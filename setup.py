import os
from setuptools import find_packages, setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a data
# string in below ...
def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


with open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'requirements.txt'))) as fp:
    install_requires = fp.read().splitlines()

setup_requirements = [
    'pytest-runner',
]

test_requirements = [
    'pytest',
    'nbformat'
]

setup(
    author='SN',
    author_email='simone.nascimento@lgim.com',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],

    name="assetallocation_arp",
    version="0.0.24",
    #version_config={
    #  "version_format": "{tag}.dev{sha}",
    #  "starting_version": "0.0.24"
    #},
    description="sist[3~[3~[3~[3~[3~",
    long_description=open('README.md').read(),
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    include_package_data = True,
    install_requires=install_requires
)
