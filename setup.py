import setuptools


with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='oanda-api',
    version='0.1.1',
    author='mniyk',
    author_email='my.name.is.yohei.kono@gmail.com',
    description='oanda api python library',
    long_description=long_description,
    url='https://github.com/mniyk/oanda-api.git',
    packages=setuptools.find_packages(),
    install_requires=['oandapyV20'])
