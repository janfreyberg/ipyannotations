# `ipyannotations`: create rich annotations in jupyter notebooks.

[![Documentation Status](https://readthedocs.org/projects/ipyannotations/badge/?version=latest)](https://ipyannotations.readthedocs.io/en/latest/?badge=latest)
[![travis CI build](https://travis-ci.com/janfreyberg/ipyannotations.svg?branch=master)](https://travis-ci.com/janfreyberg/ipyannotations)
[![Coverage Status](https://coveralls.io/repos/github/janfreyberg/ipyannotations/badge.svg?branch=master)](https://coveralls.io/github/janfreyberg/ipyannotations?branch=master)
[![Launch Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/janfreyberg/ipyannotations/master?filepath=docs/quick-start.ipynb)

The `ipyannotations` library is designed to let you create rich annotations
for your data (currently, primarily images) inside jupyter notebooks. It lets
you leverage the rich jupyter display system from python. It was designed to
integrate with `superintendent`, but does not need to.

For example, draw polygons onto images for your machine learning applications:

![interface](docs/img/interface.png)

## Installation

Start by installing `ipyannotations`:

```
$ pip install ipyannotations
```

If you are using Jupyter Lab, rather than the old Jupyter Notebook application, you will also
have to install two Jupyter Lab extensions:

## Jupyter Lab extensions

```
$ jupyter labextension install @jupyter-widgets/jupyterlab-manager ipycanvas
$ jupyter lab build
```

## ipyannotations development

It's super helpful to have other people contribute to projects like this, so
please fork this repository and make pull requests!

`ipyannotations` uses `flit` to manage the packaging, so the easiest way to use
it is to set up a virtual environment, install `ipyannotations` as a symlink,
and go from there:

```
git clone git@github.com:<your-username>/ipyannotations.git && cd ipyannotations
pre-commit install
python -m venv .venv
flit install --symlink --python .venv/bin/python
jupyter labextension install @jupyter-widgets/jupyterlab-manager ipycanvas
jupyter lab build
```
