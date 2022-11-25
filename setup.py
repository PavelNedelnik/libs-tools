from setuptools import find_packages, setup
setup(
    name='libs-tools',
    packages=find_packages(include=['libs-tools']),
    version='0.1.0',
    description='Commonly used tools for LIBS analysis',
    author='PN',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==7.2.0'],
    test_suite='tests',
)