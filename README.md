
# ipyannotations

[![Coverage Status](https://coveralls.io/repos/github/janfreyberg/ipyannotations/badge.svg?branch=main)](https://coveralls.io/github/janfreyberg/ipyannotations?branch=main)
[![Build](https://github.com/janfreyberg/ipyannotations/actions/workflows/build.yml/badge.svg)](https://github.com/janfreyberg/ipyannotations/actions/workflows/build.yml)
[![Unit tests and linting](https://github.com/janfreyberg/ipyannotations/actions/workflows/test.yml/badge.svg)](https://github.com/janfreyberg/ipyannotations/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/ipyannotations.svg)](https://badge.fury.io/py/ipyannotations)

Create rich adata annotations in jupyter notebooks.

ipyannotations provides interactive UI elements, based on ipywidgets, to allow
developers and scientists to label data right in the notebook.

ipyannotations supports many common data labelling tasks, such as image and text
classification and annotation. It also supports custom data presentation by
leveraging the Jupyter ecosystem.

[![interface](https://user-images.githubusercontent.com/4092425/132008979-2fa43ec2-1add-4376-aba9-7836509b8e8f.png)](https://user-images.githubusercontent.com/4092425/132008979-2fa43ec2-1add-4376-aba9-7836509b8e8f.png)

## Installation

You can install using `pip`:

```bash
pip install ipyannotations
```

If you are using Jupyter Notebook 5.2 or earlier, you may also need to enable
the nbextension:
```bash
jupyter nbextension enable --py [--sys-prefix|--user|--system] ipyannotations
```

## Development Installation

Create a dev environment:
```bash
conda create -n ipyannotations-dev -c conda-forge nodejs yarn python jupyterlab
conda activate ipyannotations-dev
```

Install the python. This will also build the TS package.
```bash
pip install -e ".[test, examples]"
```

When developing your extensions, you need to manually enable your extensions with the
notebook / lab frontend. For lab, this is done by the command:

```
jupyter labextension develop --overwrite .
yarn run build
```

For classic notebook, you need to run:

```
jupyter nbextension install --sys-prefix --symlink --overwrite --py ipyannotations
jupyter nbextension enable --sys-prefix --py ipyannotations
```

Note that the `--symlink` flag doesn't work on Windows, so you will here have to run
the `install` command every time that you rebuild your extension. For certain installations
you might also need another flag instead of `--sys-prefix`, but we won't cover the meaning
of those flags here.

### How to see your changes
#### Typescript:
If you use JupyterLab to develop then you can watch the source directory and run JupyterLab at the same time in different
terminals to watch for changes in the extension's source and automatically rebuild the widget.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
yarn run watch
# Run JupyterLab in another terminal
jupyter lab
```

After a change wait for the build to finish and then refresh your browser and the changes should take effect.

#### Python:
If you make a change to the python code then you will need to restart the notebook kernel to have it take effect.
