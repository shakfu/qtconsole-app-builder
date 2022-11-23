# qtconsole-app-builder

A python script to build [qtconsole](https://github.com/jupyter/qtconsole) as a macOS `.app` bundle using [py2app](https://github.com/ronaldoussoren/py2app).


## Usage

It's pretty simple:

```bash

python3 create_qtconsole_app.py

```

This will create a virtualenv called `qtenv`, and after it concludes you should find `QtConsoleApp.app` in `qtenv/dist`.


## Shrinking the Final Bundle

The current build is not optimized for space. The quickest and biggest post-build step is to remove `QtWebEngineCore.framework` from the final product.



## TODO

- [x] include matplotlib
- [x] include numpy
- [ ] shrink final `.app` bundle via post-build shrink function
- [ ] test test test



## Licensing

The contents of this repo are placed in the public domain.
