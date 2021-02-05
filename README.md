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

On older versions of Jupyter Lab, rather than the old Jupyter Notebook
application, you will also have to install two Jupyter Lab extensions:

```
$ jupyter labextension install @jupyter-widgets/jupyterlab-manager ipycanvas
$ jupyter lab build
```

## Development installation

It's super helpful to have other people contribute to projects like this, so
please fork this repository and make pull requests!

For a development installation (requires [Node.js](https://nodejs.org) and
[Yarn version 1](https://classic.yarnpkg.com/)),

    $ git clone https://github.com/janfreyberg/ipyannotations.git
    $ cd ipyannotations
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --overwrite --sys-prefix ipyannotations
    $ jupyter nbextension enable --py --sys-prefix ipyannotations

When actively developing your extension for JupyterLab, run the command:

    $ jupyter labextension develop --overwrite ipyannotations

Then you need to rebuild the JS when you make a code change:

    $ cd js
    $ yarn run build

You then need to refresh the JupyterLab page when your javascript changes.
