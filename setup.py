from setuptools import setup, find_packages

setup(
    name='flockbot',
    version='1.0.4dev',
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
    # packages=['flockbot'],
    packages=find_packages(exclude=['contrib', 'docs']),
    install_requires=['sqlalchemy', 'praw']
)
