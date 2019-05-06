from setuptools import setup

setup(
    name='IntuitiveUnderstanding',
    version='0.1',
    author='Signaltonsalat',
    description='Dark Souls Bot',
    license='MIT',
    keywords='games bot ai',
    packages=['intund'],
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'intund = intund.main:cli',
        ],
    },
    install_requires=[
        'click',
        'pynput',
        'pywin32',
        'psutil',
    ],
)
