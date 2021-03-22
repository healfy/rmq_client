import os.path

from setuptools import find_packages, setup

from clients import __version__

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
REQUIREMENTS = os.path.join(BASE_DIR, 'requirements.txt')


def get_requirements(path):
    with open(path) as f:
        lines = map(str.strip, f.read().splitlines())
        return list(filter(bool, lines))


setup(
    name='rmq_client',
    version=__version__,
    description='Base async clients implementation for RabbitMQ',
    author='K. Zavadsky',
    author_email='healfy92@gmail.com',
    packages=find_packages(exclude=('tests', )),
    install_requires=get_requirements(REQUIREMENTS),
    zip_safe=False,
)
