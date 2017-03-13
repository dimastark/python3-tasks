import setuptools


setuptools.setup(
    name='pylife',
    version='0.2',
    description="Conway's Life",
    author='dimastark',
    author_email='dstarkdev@gmail.com',
    entry_points={
        'console_scripts': [
            'pylife = pylife.newlife:main',
        ]
    },
    packages=setuptools.find_packages(
        '.',
        exclude=[
            '*.tests', '*.tests.*', 'tests.*', 'tests',
        ],
    ),
    package_data={'pylife': ['saves.txt']},
    include_package_data=False,
    install_requires=[
        'setuptools',
        'pygame',
    ],
    tests_require=['nose'],
    test_suite='nose.collector',
)
