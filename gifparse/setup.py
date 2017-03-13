import setuptools


setuptools.setup(
    name='gifparse',
    version='0.1',
    description='Simple python3 gif parser with PyQt5 GUI',
    author='dimastark',
    author_email='dstarkdev@gmail.com',
    entry_points={
        'console_scripts': [
            'gifparse = gifparse.gui:main',
        ]
    },
    packages=setuptools.find_packages(
        '.',
        exclude=[
            '*.tests', '*.tests.*', 'tests.*', 'tests',
        ],
    ),
    package_data={'': ['test_files']},
    include_package_data=False,
    install_requires=[
        'setuptools',
    ],
    tests_require=['nose'],
    test_suite='nose.collector',
)
