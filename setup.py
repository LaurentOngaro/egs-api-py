import setuptools
from setuptools import setup
import sys
from pathlib import Path
from egs_api import __name__, __version__, __codename__, __license__, __author__, __author_email__, __description__, __url__

if sys.version_info < (3, 9):
    sys.exit('python 3.9 or higher is required for this project')

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

current_folder = Path(__file__).parent

# Read __long_description__ from README.md
######################
__long_description__ = Path.joinpath(current_folder, 'README.md').read_text()
# add information about the version and codename in the PyPI page because codename s not available by default
__long_description__ += f'\n\n {__name__} ## version:{__version__} ## codename: {__codename__}'
# __long_description__ = ''.join(__long_description__[8:16])  # keep only description text

setup(
    name=__name__,
    version=__version__,
    license=__license__,
    author=__author__,
    author_email=__author_email__,
    description=__description__,
    long_description=__long_description__,
    long_description_content_type='text/markdown',
    url=__url__,
    packages=setuptools.find_packages(),
    # data_files=[('', ['UEVaultManager/assets/UEVM_200x200.png','UEVaultManager/assets/main.ico'])],
    package_data={'': ['assets/*']},
    python_requires='>=3.9',
    classifiers=[
        'License :: OSI Approved :: MIT License',  #
        'Programming Language :: Python :: 3.9',  #
        'Programming Language :: Python :: 3.10',  #
        'Programming Language :: Python :: 3.11',  #
        'Programming Language :: Python :: 3.12',  #
        'Operating System :: OS Independent',  #
        'Development Status :: 4 - Beta'
        #'Development Status :: 5 - Production/Stable'
    ]
)
if __name__ == '__main__':
    setup()
