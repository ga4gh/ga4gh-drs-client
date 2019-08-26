import setuptools
import codecs

NAME = "ga4gh-drs-client"
VERSION = "0.1.0"
AUTHOR = "Jeremy Adams"
EMAIL = "jeremy.adams@ga4gh.org"

try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name=='mbcs')
    codecs.register(func)

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    "click",
    "crc32c",
    "PyYAML",
    "requests",
    "tqdm"
]

setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description="A client for accessing data from Data Repository Service "
        + "(DRS) web services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ga4gh/ga4gh-drs-client",
    package_data={'': ['*.yml']},
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            'drs=ga4gh.drs.entrypoint:main',
        ]
    }
    ,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ),
)
