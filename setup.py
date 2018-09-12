from setuptools import setup, find_packages

setup(
    name='tdAmeritrade',
    version='0.0.1',
    description='Helper libraries for applications consuming TDAmeritrade API',
    url='',
    author='Ryeland Gongora',
    author_email='rsgmon@gmail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['aiohttp', 'requests'],
    zip_safe=False)
