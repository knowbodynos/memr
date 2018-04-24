from setuptools import setup

setup(
    name='memr',
    packages=['memr'],
    include_package_data=True,
    install_requires=[
        'flask',
        'imgurpython',
        'random',
    ],
)