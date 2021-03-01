from setuptools import setup, find_packages


setup(name='AeroBemt',
      version='0.1',
      url='https://github.com/marcy3ait/ProjetoFinal#-triplex-aviation-corp-',
      license='MIT',
      author='Triplex Aviation',
      author_email='marcy.borges@unesp.br',
      description='impletação do método BEMT',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md', encoding='utf-8').read(),
      zip_safe=False)