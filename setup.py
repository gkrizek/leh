from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name="leh",
    version="0.1.0",
    description="Lambda Exception Helper",
    long_description=readme(),
    author="Graham Krizek",
    author_email="graham@krizek.io",
    url="https://github.com/gkrizek/leh",
    license="MIT",
    packages="leh",
    install_requires=[
        "boto3"
    ],
    classifiers=[
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 3
    ],
    keywords="aws lambda unhandled exception logging error"
)
