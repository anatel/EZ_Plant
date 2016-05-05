from setuptools import setup
import sys

install_requires = ['Flask==0.10.1', 'enum34==1.1.2', 'ipython==4.1.2', 'pymongo==3.2.2', 'passlib==1.6.5']

setup(name='ez_plant',
    version='0.0.1',
    description='Webapp for managing and controlling auto irrigated plants',
    install_requires=install_requires,
    license='BSD',
    packages=['ez_plant'],
    entry_points=dict(console_scripts=['ez_plant=ez_plant.app:main']),
    zip_safe=True)
