import setuptools


setuptools.setup(
    name='whuts-solver',
    entry_points=dict(
        console_scripts=['whuts-solver = whuts_solver:entry_point']),
    install_requires=['exact-cover'],
    include_package_data=True,
    packages=setuptools.find_packages())
