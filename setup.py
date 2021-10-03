from setuptools import setup, find_packages

setup(
  name='csvfit',
  version='1.0.0',
  author='Dominik Hanko',
  author_email='dominik.hanko91@gmail.com',
  description='system identification with csv files as inputs',
  packages=find_packages(include=['fit', 'fit.*', 'test', 'test.*']),
  package_data={'fit': ['test/example.zip']},
  install_requires=[
    'click >=8.0.1',
    'scipy >=1.7.1', 
    'matplotlib >=3.4.3',
    'numpy >=1.21.2'
  ],
  entry_points={
    'console_scripts': [
      'fitpt=fit.fitpt:main',
      'fitarx=fit.fitarx:main'
    ],
  },
)