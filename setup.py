from setuptools import setup, find_packages, Extension

#######################################
# Prepare list of compiled extensions #
#######################################

extensions = []


#########
# Setup #
#########

setup(
    name='pyk2',
    version='0.0.0',
    description='Python wrapped sixtrack k2 scattering routines',
    url='https://github.com/giadarol/IsolatedK2',
    author='Giovanni Iadarola',
    packages=find_packages(),
    ext_modules = extensions,
    include_package_data=True,
    install_requires=[
        'numpy>=1.0',
        'scipy',
        ]
    )
