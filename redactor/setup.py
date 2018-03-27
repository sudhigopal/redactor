from setuptools import setup,find_packages

setup(
        name = 'redactor',
        version = '1.0',
        author = 'Sudhindra Gopal',
        author_email = 'sudhi@ou.edu',
        package = find_packages(exclude=('tests','docs')),
        tests_require = ['pytest'],
        setup_require = ['pytest-runner']
    )

