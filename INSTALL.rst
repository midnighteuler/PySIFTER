==============
 Installation
==============

dependencies
------------

Python 2.7
~~~~~~~~~~

``argparse`` module required.

docutils
~~~~~~~~

docutils is required only to compile docs::

 wget "http://prdownloads.sourceforge.net/docutils/docutils-0.7.tar.gz?download" && \
 tar -xf docutils-0.7.tar.gz && \
 cd docutils-0.7 && \
 python setup.py install

biopython 1.59
----------------

Download and install using git::

 git clone git@github.com:biopython/biopython.git
 cd biopython
 python setup.py install


