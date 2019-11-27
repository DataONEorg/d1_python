Bootstrap
=========

This small package holds utilities that have no d1_python dependencies, used for various setup and build tasks.

The module members are available directly from ``__init__``.

pkg
~~~

This is the canonical source of paths for scripts that iterate over all d1_python packages.

The paths are all absolute and in order of fewest to most dependencies. Later packages depend on one or more of the earlier packages.

d1_doc
------

All d1_python packages have a section of documentation automatically generated from docstrings by ``autodoc``. The main quirk of ``autodoc``is that, instead of parsing the modules, it imports them. For modules to be importable, all their dependencies have to be installed (unless one wants to mess around with mocking out the imports). So ``d1_doc`` depends on all the packages in d1_python in addition to Sphinx and the Sphinx extensions we use.
