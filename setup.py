from setuptools import setup, find_packages


setup(name='aerobemt',
      version='1.0',
      url='https://github.com/marcy3ait/',
      license='MIT',
      author='Triplex Aviation',
      author_email='marcy.borges@unesp.br',
      description='impletação do método BEMT',
      packages=find_packages(),
      long_description=open('README.md', encoding='utf-8').read(),
      zip_safe=False)