#!/usr/bin/env python3

"""create_qtconsole_app.py

A proof-of-concept script to create a minimal qtconsole macos .app bundle
using py2app.

"""

LAUNCHER_PY = """
import re
import sys
from qtconsole.qtconsoleapp import main
if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\\.pyw|\\.exe)?$', '', sys.argv[0])
    sys.exit(main())
"""


PACKAGES = [
    "pygments",
    "zmq",
    "jedi",
    "parso",
    "qtconsole",
    "ipykernel",
    "IPython",
]


INCLUDES = [
    "pyqt5",
    "qtconsole",
    # also required
    "asttokens",
    "ipykernel_launcher",
]

EXCLUDES = [
    "black",
    "build",
    "docutils",
    "flexx",
    "jupyter",
    "meta",
    "nbformat",
    "pyenchant",
    "pyflakes",
    "pylint",
    "pyshortcuts",
    "sphinx", # including this causes ImportError: No module named 'sphinxcontrib'
    "tk",
    "debugpy",
]

SETUP_REQUIRES = [
    "py2app",
    "pyqt5",
    "qtconsole",
    "pygments",
    "pyzmq",
]

SETUP_EXTRA = [

]

SETUP_PY = """
from setuptools import setup
setup(
    app=['{app}'],
    data_files={data_files},
    options=dict(py2app={options}),
    setup_requires={setup_requires}
)
"""

QTCONSOLE_DEPS = [
    "appnope",
    "asttokens",
    "backcall",
    "debugpy",
    "decorator",
    "entrypoints",
    "executing",
    "ipykernel",
    "ipython",
    "ipython-genutils",
    "jedi",
    "jupyter-client",
    "jupyter-core",
    "matplotlib-inline",
    "nest-asyncio",
    "packaging",
    "parso",
    "pexpect",
    "pickleshare",
    "platformdirs",
    "prompt-toolkit",
    "psutil",
    "ptyprocess",
    "pure-eval",
    "pygments",
    "pyparsing",
    "python-dateutil",
    "pyzmq",
    "qtconsole"
    "qtpy",
    "six",
    "stack-data",
    "tornado",
    "traitlets",
    "wcwidth",
]

import os
import shutil
import sysconfig


class QtConsoleAppBuilder:
    def __init__(self, app: str, **options):
        self.app = app
        self.venv = options.get("venv", "qtenv")
        self.packages = options.get("packages", PACKAGES)
        self.includes = options.get("includes", INCLUDES)
        self.excludes = options.get("excludes", EXCLUDES)
        self.setup_requires = options.get("setup_requires", SETUP_REQUIRES)
        self.py_ver = sysconfig.get_config_var("py_version_short")

    def cmd(self, shellcmd, *args, **kwds):
        os.system(shellcmd.format(*args, **kwds))

    def vcmds(self, shellcmds, *args, **kwds):
        shellcmd = " && ".join(shellcmds)
        os.system(shellcmd)

    def remove_tests(self, testdir):
        shutil.rmtree(testdir)
        print('removed testdir:', testdir)

    def create_launcher(self, path):
        with open(path, "w") as f:
            f.write(LAUNCHER_PY)

    def create_setup(self, path):
        setup_py = SETUP_PY.format(
            app=self.app,
            data_files=[],
            options=dict(
                includes=self.includes,
                excludes=self.excludes,
                packages=self.packages,
            ),
            setup_requires=self.setup_requires,
        )
        with open(path, "w") as f:
            f.write(setup_py)

    def build(self):
        self.vcmds(
            [
                f"virtualenv {self.venv}",
                f"source {self.venv}/bin/activate",
                "pip install leo py2app",
            ]
        )
        self.create_launcher(f"{self.venv}/{self.app}")
        # self.remove_tests(
        #     f"{self.venv}/lib/python{self.py_ver}/site-packages/"
        # )
        self.create_setup(f"{self.venv}/setup.py")
        self.vcmds(
            [
                f"source {self.venv}/bin/activate",
                f"cd {self.venv}",
                # f"python setup.py py2app",
                f"python setup.py py2app --iconfile ../resources/icons/app.icns",
            ]
        )


if __name__ == "__main__":
    builder = QtConsoleAppBuilder(app="QtConsoleApp.py")
    builder.build()
