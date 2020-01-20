# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# flake8: noqa

import pkg_resources


# -- Project information -----------------------------------------------------

project = "ipyannotations"
copyright = "2020, Jan Freyberg"
author = "Jan Freyberg"

# The full version, including alpha/beta/rc tags
version = pkg_resources.get_distribution("ipyannotations").version
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.

master_doc = "index"

extensions = ["m2r", "nbsphinx", "sphinx.ext.napoleon"]

source_suffix = [".rst", ".md"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_logo = "img/logo.png"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]

nbsphinx_prolog = r"""
{% set docname = 'docs/' + env.doc2path(env.docname, base=None) %}
.. only:: html

    .. role:: raw-html(raw)
        :format: html

    .. nbinfo::
        This page was generated from `{{ docname }}`__. All widgets shown here
        are "static", and interacting with them won't change the rest of the
        widgets. You can find a fully interactive online version here:
        :raw-html:`<a href="https://mybinder.org/v2/gh/janfreyberg/ipyannotations/{{ env.config.release }}?filepath={{ docname }}"><img alt="Binder badge" src="https://mybinder.org/badge_logo.svg" style="vertical-align:text-bottom"></a>`

    __ https://github.com/janfreyberg/ipyannotations/blob/{{ env.config.release }}/{{ docname }}

"""
