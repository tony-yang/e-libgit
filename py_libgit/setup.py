from setuptools import setup, find_packages

setup(
    name='pylibgit',
    version='0.1',
    packages=find_packages(),

    entry_points = {
        'console_scripts': ['pygit=py_libgit.cli.git:main']
    },
    
    install_requires=[
        'coverage'
    ]
)
