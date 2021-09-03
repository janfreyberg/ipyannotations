(installation)=

# Installation

The simplest way to install ipyannotations is via pip:

```
pip install ipyannotations
```

If you installed via pip, and notebook version \< 5.3, you will also have to
install / configure the front-end extension as well. If you are using classic
notebook (as opposed to Jupyterlab), run:

```
jupyter nbextension install [--sys-prefix / --user / --system] --py ipyannotations

jupyter nbextension enable [--sys-prefix / --user / --system] --py ipyannotations
```

with the [appropriate flag]. If you are using a Jupyterlab version below 3.0,
install the lab extension with:

```
jupyter labextension install ipyannotations
jupyter lab build
```

% links

[appropriate flag]: https://jupyter-notebook.readthedocs.io/en/stable/extending/frontend_extensions.html#installing-and-enabling-extensions
