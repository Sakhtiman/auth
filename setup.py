from setuptools import setup, find_packages

setup(
    name='Resauth',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'fastapi==0.68.0',
        'sqlalchemy==1.4.30',
        'pyjwt==2.3.0',
        'uvicorn==0.15.0',
        'passlib==1.7.4',
        'python-jose==3.3.0',
    ],
    entry_points={
        'console_scripts': [
            'resolute = resolute.main:app'
        ],
    },
)
