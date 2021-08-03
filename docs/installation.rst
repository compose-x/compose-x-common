.. highlight:: shell

============
Installation
============


Stable release
===============

To install Compose-X Commons Lib, run this command in your terminal:

.. code-block:: console

    $ pip install compose_x_common

This is the preferred method to install Compose-X Commons Lib, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

Extras
========

If you wish to use some additional functions, which rely on 3rd party libraries, you can install the following:

compose_x_common[aws]
------------------------

Allows to use the compose_x_common.aws package.
Installs boto3

From sources
==============

The sources for Compose-X Commons Lib can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/compose-x/compose_x_common

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/compose-x/compose_x_common/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/compose-x/compose_x_common
.. _tarball: https://github.com/compose-x/compose_x_common/tarball/master
.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
