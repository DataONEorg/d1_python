# Makefile for Sphinx documentation
#

# usage: sphinx-build [OPTIONS] SOURCEDIR OUTPUTDIR [FILENAMES...]
# 
# Generate documentation from source files. sphinx-build generates documentation
# from the files in SOURCEDIR and places it in OUTPUTDIR. It looks for 'conf.py'
# in SOURCEDIR for the configuration settings. The 'sphinx-quickstart' tool may
# be used to generate template files, including 'conf.py' sphinx-build can
# create documentation in different formats. A format is selected by specifying
# the builder name on the command line; it defaults to HTML. Builders can also
# perform other tasks related to documentation processing. By default,
# everything that is outdated is built. Output only for selected files can be
# built by specifying individual filenames.
# 
# positional arguments:
#   sourcedir         path to documentation source files
#   outputdir         path to output directory
#   filenames         a list of specific files to rebuild. Ignored if -a is
#                     specified
# 
# optional arguments:
#   -h, --help        show this help message and exit
#   --version         show program's version number and exit
# 
# general options:
#   -b BUILDER        builder to use (default: html)
#   -a                write all files (default: only write new and changed
#                     files)
#   -E                don't use a saved environment, always read all files
#   -d PATH           path for the cached environment and doctree files
#                     (default: OUTPUTDIR/.doctrees)
#   -j N              build in parallel with N processes where possible (special
#                     value "auto" will set N to cpu-count)
# 
# build configuration options:
#   -c PATH           path where configuration file (conf.py) is located
#                     (default: same as SOURCEDIR)
#   -C                use no config file at all, only -D options
#   -D setting=value  override a setting in configuration file
#   -A name=value     pass a value into HTML templates
#   -t TAG            define tag: include "only" blocks with TAG
#   -n                nit-picky mode, warn about all missing references
# 
# console output options:
#   -v                increase verbosity (can be repeated)
#   -q                no output on stdout, just warnings on stderr
#   -Q                no output at all, not even warnings
#   --color           do emit colored output (default: auto-detect)
#   -N, --no-color    do not emit colored output (default: auto-detect)
#   -w FILE           write warnings (and errors) to given file
#   -W                turn warnings into errors
#   --keep-going      With -W, keep going when getting warnings
#   -T                show full traceback on exception
#   -P                run Pdb on exception

MAKEFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
CUR_DIR_PATH := $(dir $(MAKEFILE_PATH))
D1_ROOT_PATH := $(realpath $(CUR_DIR_PATH)/../../../)

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build -j auto --color
PAPER         =
BUILDDIR      = ./doc/build
GENDIR        = $(BUILDDIR)/generated
SOURCE        = ./doc/rst
CONFIG        = $(SOURCE)

# Internal variables.
PAPEROPT_a4     = -D latex_paper_size=a4
PAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS   = -c $(CONFIG) -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) $(SOURCE)

.PHONY: help clean html dirhtml pickle json htmlhelp qthelp latex changes linkcheck doctest

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html      to make standalone HTML files"
	@echo "  dirhtml   to make HTML files named index.html in directories"
	@echo "  pickle    to make pickle files"
	@echo "  json      to make JSON files"
	@echo "  htmlhelp  to make HTML files and a HTML help project"
	@echo "  qthelp    to make HTML files and a qthelp project"
	@echo "  latex     to make LaTeX files, you can set PAPER=a4 or PAPER=letter"
	@echo "  changes   to make an overview of all changed/added/deprecated items"
	@echo "  linkcheck to check all external links for integrity"
	@echo "  doctest   to run all doctests embedded in the documentation (if enabled)"

clean:
	-rm -rf $(BUILDDIR)/* $(GENDIR)/*

html:
	cd ${D1_ROOT_PATH}; $(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

dirhtml:
	cd ${D1_ROOT_PATH}; $(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) $(BUILDDIR)/dirhtml
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/dirhtml."

pickle:
	cd ${D1_ROOT_PATH}; $(SPHINXBUILD) -b pickle $(ALLSPHINXOPTS) $(BUILDDIR)/pickle
	@echo
	@echo "Build finished; now you can process the pickle files."

json:
	cd ${D1_ROOT_PATH}; $(SPHINXBUILD) -b json $(ALLSPHINXOPTS) $(BUILDDIR)/json
	@echo
	@echo "Build finished; now you can process the JSON files."

htmlhelp:
	cd ${D1_ROOT_PATH}; $(SPHINXBUILD) -b htmlhelp $(ALLSPHINXOPTS) $(BUILDDIR)/htmlhelp
	@echo
	@echo "Build finished; now you can run HTML Help Workshop with the" \
	      ".hhp project file in $(BUILDDIR)/htmlhelp."

qthelp:
	cd ${D1_ROOT_PATH}; $(SPHINXBUILD) -b qthelp $(ALLSPHINXOPTS) $(BUILDDIR)/qthelp
	@echo
	@echo "Build finished; now you can run "qcollectiongenerator" with the" \
	      ".qhcp project file in $(BUILDDIR)/qthelp, like this:"
	@echo "# qcollectiongenerator $(BUILDDIR)/qthelp/PyD1.qhcp"
	@echo "To view the help file:"
	@echo "# assistant -collectionFile $(BUILDDIR)/qthelp/PyD1.qhc"

latex:
	cd ${D1_ROOT_PATH}; $(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(BUILDDIR)/latex
	@echo
	@echo "Build finished; the LaTeX files are in $(BUILDDIR)/latex."
	@echo "Run \`make all-pdf' or \`make all-ps' in that directory to" \
	      "run these through (pdf)latex."

changes:
	cd ${D1_ROOT_PATH}; $(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) $(BUILDDIR)/changes
	@echo
	@echo "The overview file is in $(BUILDDIR)/changes."

linkcheck:
	cd ${D1_ROOT_PATH}; $(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(BUILDDIR)/linkcheck
	@echo
	@echo "Link check complete; look for any errors in the above output " \
	      "or in $(BUILDDIR)/linkcheck/output.txt."

doctest:
	cd ${D1_ROOT_PATH}; $(SPHINXBUILD) -b doctest $(ALLSPHINXOPTS) $(BUILDDIR)/doctest
	@echo "Testing of doctests in the sources finished, look at the " \
	      "results in $(BUILDDIR)/doctest/output.txt."
