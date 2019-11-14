from setuptools import setup, find_packages

setup(
    name="xorsearch",
    version="3.0.0",
    author="Marcus LaFerrera (@mlaferrera)",
    url="https://github.com/PUNCH-Cyber/stoq-plugins-public",
    license="Apache License 2.0",
    description="Scan a payload using xorsearch",
    packages=find_packages(),
    include_package_data=True,
    test_suite='tests',
    tests_require=['asynctest==0.13.0'],
)
