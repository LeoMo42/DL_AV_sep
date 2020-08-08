from setuptools import setup
import sys

if sys.version_info < (3,):
    sys.exit('Sorry, Python3 is required.')

with open('requirements.txt') as f:
    reqs = f.read()

setup(
    name='av_sep',
    version='0.0.1',
    description='av separate',
    packages=['av_sep'],
    install_requires=reqs.strip().split('\n'),
    include_package_data=True,
)
