#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function
from glob import glob
import os
from os.path import join as pjoin
from setuptools import setup, find_packages


from jupyter_packaging import (
    create_cmdclass,
    install_npm,
    ensure_targets,
    combine_commands,
    get_version,
)

HERE = os.path.dirname(os.path.abspath(__file__))


# The name of the project
name = "ipyannotations"

# Get the version
version = get_version(pjoin(name, "_version.py"))


# Representative files that should exist after a successful build
jstargets = [
    pjoin(HERE, name, "nbextension", "index.js"),
    pjoin(HERE, "lib", "plugin.js"),
]


package_data_spec = {name: ["nbextension/**", "labextension/**"]}


data_files_spec = [
    (
        "share/jupyter/nbextensions/ipyannotations",
        "ipyannotations/nbextension",
        "**",
    ),
    (
        "share/jupyter/labextensions/ipyannotations",
        "ipyannotations/labextension",
        "**",
    ),
    ("share/jupyter/labextensions/ipyannotations", ".", "install.json"),
    ("etc/jupyter/nbconfig/notebook.d", ".", "ipyannotations.json"),
]


cmdclass = create_cmdclass(
    "jsdeps",
    package_data_spec=package_data_spec,
    data_files_spec=data_files_spec,
)
cmdclass["jsdeps"] = combine_commands(
    install_npm(HERE, build_cmd="build:prod", npm=["yarn"]),
    ensure_targets(jstargets),
)


setup_args = dict(
    name=name,
    description="Create rich adata annotations in jupyter notebooks.",
    version=version,
    scripts=glob(pjoin("scripts", "*")),
    cmdclass=cmdclass,
    packages=find_packages(where="."),
    # package_dir={"": "src/"},
    author="Jan Freyberg",
    author_email="jan.freyberg@gmail.com",
    url="https://github.com/janfreyberg/ipyannotations",
    license="MIT",
    platforms="Linux, Mac OS X, Windows",
    keywords=["Jupyter", "Widgets", "IPython"],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Jupyter",
    ],
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "ipywidgets>=7.0.0",
        "ipycanvas>=0.13.1",
        "palettable",
        "Pillow",
        "numpy",
        "requests",
        "ipyevents",
    ],
    extras_require={
        "test": [
            "pytest>=6.0",
            "pytest-cov",
            "nbval",
            "coverage",
            "coveralls",
            "pytest-cov",
            "hypothesis",
            "pytest-check",
            "mypy>=0.910",
            "pytest-mock",
            "flake8",
            "black",
            "types-requests",
            "testver>=0.3.1",
        ],
        "dev": [
            "black",
            "flake8",
            "pre-commit",
            "jupyterlab",
            "notebook",
            "rope",
            "docargs",
            "jupyter_packaging",
        ],
        "examples": [
            # Any requirements for the examples to run
        ],
        "doc": [
            "sphinx>=4.0",
            "sphinx_rtd_theme",
            "matplotlib",
            "nbsphinx",
            "myst-parser>=0.12.9",
            "nbsphinx_link",
            "jupyter_sphinx",
        ],
    },
    entry_points={},
)

if __name__ == "__main__":
    setup(**setup_args)
