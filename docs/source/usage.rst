Usage
==========================

The DRS client is executed on the command-line via the following structure:

.. code-block:: bash

    drs get [OPTIONS] URL OBJECT_ID

where :code:`[OPTIONS]` represents a set of optional command-line parameters, 
and :code:`URL` and :code:`OBJECT_ID` represent two position-specific arguments.

Arguments and Options
----------------------

Required command-line arguments:

.. csv-table:: ga4gh-drs-client required arguments
   :header: "Parameter", "Description"
   :widths: 5 20

   "URL", "Base URL to DRS service (up to but excluding the DRS BasePath '/ga4gh/drs/v1')"
   "OBJECT_ID", "DRS object identifier"

Optional command-line options:

.. csv-table:: ga4gh-drs-client options
   :header: "Parameter", "Short Name", "Description"
   :widths: 2 10 20

   "-t", "--authtoken", "Value of OAuth 2.0 Authorization: Bearer token"
   "-d", "--download", "Flag. If set, download object bytes"
   "-x", "--expand", "Flag. If set, program will recursively traverse inner bundles within the root bundle"
   "-l", "--logfile", "File to which logs should be written"
   "-o", "--output-dir", "Directory to write downloaded files"
   "-m", "--output-metdata", "File to write object metadata (printed to stdout by default)"
   "-S", "--silent", "Flag. If set, don't output any messages to console or log file"
   "-s", "--suppress-ssl-verify", "Flag. If set, suppress ssl certification verificiation (NOT RECOMMENDED)"
   "-v", "--validate-checksum", "Flag. If set, perform checksum validation on downloaded objects"
   "-V", "--verbosity", "DEBUG|INFO|WARNING|ERROR Control verbosity of logging"

Example Usage
--------------

1. Basic Usage, get DRS object and print metadata to screen

.. code-block:: bash
    
    drs get https://exampledrs.com/ a02568e6-11f8-4493-9880-f51823df09b8

2. Write metadata to an output file

.. code-block:: bash

    drs get -m metadata.json https://exampledrs.com/ a02568e6-11f8-4493-9880-f51823df09b8

3. Download object bytes, writing output files to the "output" directory

.. code-block:: bash

    drs get -d -o output https://exampledrs.com/ a02568e6-11f8-4493-9880-f51823df09b8

4. Use an auth token to access DRS object data/metadata

.. code-block:: bash

    drs get -d -o output -t P8vNFYh6jC https://exampledrs.com/ a02568e6-11f8-4493-9880-f51823df09b8

5. Write debug, info, warning, and error logs to a log file

.. code-block:: bash

    drs get -l logfile.txt -V DEBUG https://exampledrs.com/ a02568e6-11f8-4493-9880-f51823df09b8
