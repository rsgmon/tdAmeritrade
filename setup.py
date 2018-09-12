from setuptools import setup, find_packages


try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

reqs = parse_requirements('./requirements.txt', session=False)
install_requires = [str(ir.req) for ir in reqs]


setup(name='tdAmeritrade',
      version='0.0.1',
      description='Helper libraries for applications consuming TDAmeritrade API',
      url='',
      author='Ryeland Gongora',
      author_email='rsgmon@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      install_requires = install_requires,
      zip_safe=False)