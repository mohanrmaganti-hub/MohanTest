from setuptools import setup, find_packages

setup(
    name='servicenow_etl',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pyodbc',
        'python-dotenv',
        'pandas',
        'pyyaml',
        'tenacity'
    ]
)
