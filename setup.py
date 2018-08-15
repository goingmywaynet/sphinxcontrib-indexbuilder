from setuptools import setup, find_packages
import sys
sys.path.append('./sphinxcontrib')

f = open('README.rst', 'r')
try:
    long_desc = f.read()
finally:
    f.close()
    
requires = ['Sphinx>=1.0']

setup(
    name='sphinxcontrib-indexbuilder',
    version='0.1',
    description='sphinx index building tools',
    long_description=long_desc,
    url='',
    author='Joey Chen',
    author_email='joey-tech@goingmyway.net',
    classifiers=[
          # How mature is this project? Common values are
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',

          # Indicate who your project is intended for
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',

          # Pick your license as you wish (should match "license" above)
          'License :: OSI Approved :: MIT License',
          'Natural Language :: Japanese',
          'Operating System :: Microsoft :: Windows',
          'Programming Language :: Python',
          'Topic :: Documentation',
          'Topic :: Utilities',
    ],
    keywords = 'sphinx,sphinxcontrib,smb,windows,link,share',
    packages=find_packages(),
    install_requires=requires,
    license='MIT',
    platforms='any',
    include_package_data=True,
    #namespace_packages=['sphinxcontrib'],
    entry_points = {
          # commandline tool setup
          'console_scripts': ['SearchBuildTargets=indexbuilder.SearchBuildTargets:main'],
    },
    zip_safe=False
)
