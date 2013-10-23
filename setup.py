from setuptools import setup, find_packages

setup(
    name='django-timecop',
    packages=find_packages(),
    include_package_data=True,
    version='0.0.1',
    description='TODO',
    long_description='TODO',
    author='Andrew Sibley',
    url='TODO',
    license='BSD',
    install_requires=[
        'distribute',
        'django>=1.5.4',
    ],

)
