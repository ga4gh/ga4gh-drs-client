Installation
============

This section provides instructions on how to install the DRS command-line
client.

As a prerequisite, python 3 and pip must be installed on your system. The 
application can be installed by running the following from the command line. 

1. Clone the latest build from https://github.com/ga4gh/ga4gh-drs-client.git

.. code-block:: bash

    git clone https://github.com/ga4gh/ga4gh-drs-client.git

2. Enter ga4gh-drs-client directory and install

.. code-block:: bash

    cd ga4gh-drs-client
    python setup.py install

3. Confirm installation by executing the drs command

.. code-block:: bash

    drs get

The `next article <usage.html>`_ explains how to run the drs client.