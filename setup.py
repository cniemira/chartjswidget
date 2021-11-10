import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "chartjswidget",
    version = "0.0.1",
    author = "CJ Niemira",
    author_email = "siege@siege.org",
    description = ("A very thin wrapper around chart.js for PySide6"),
    long_description=read('README.md'),
    keywords = "qt pyside chart webview",
    license = "MIT",
    url = "https://github.com/cniemira/chartjswidget",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Widget Sets",
    ],
    install_requires=['PySide6'],
    packages=['chartjswidget'],
    package_data={
        'chartjswidget': [
            'chart-3.8.0.min.js',
            'page.html'
            ],
    }
)
