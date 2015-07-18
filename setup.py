from setuptools import setup

setup(
    name='flockbot',
    version='1.0dev',
    author='Stan Janssen',
    author_email='stanjanssen@outlook.com',
    url='https://github.com/FlockBots/flockbot',
    description='A Reddit bot as a Python module based on PRAW.',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.4',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent'
    ],
    keywords='reddit bot base',
    packages=['flockbot'],
    install_requires=['sqlalchemy', 'praw']
)