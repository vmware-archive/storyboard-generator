from setuptools import setup, find_packages

setup(
    name='storyboardgenerator',
    version='1.1',
    install_requires=['attrs'],
    tests_require=["pytest", "pytest-catchlog", "pytest-flakes", "pytest-pep8"],
    packages=find_packages(),
    author='Team Awesomness',
    author_email='awesomeness@localhost.com',
)
