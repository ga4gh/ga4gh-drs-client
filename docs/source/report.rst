Report and Output
==================

At a high level, the DRS client generates 3 different types of data when
executed:

1. Requested object metadata
2. Downloaded files
3. Download status report

Requested object metadata
--------------------------

Metadata for the requested DRS object is downloaded as JSON. By default, 
metadata is printed to screen. If the :code:`-m FILENAME` option is used on 
the command-line, output will be written to the specified file.  

Downloaded files
----------------

If the :code:`-d` flag is used on the command-line, the client will attempt to
download bytes for the DRS object. If the requested object id was a bundle,
it will download bytes for all objects in the bundle.

By default, downloaded files are written to the current working directory. If
the :code:`-o DIRECTORY` option is used on the command-line, downloaded files
are written to the user-specified output directory.

Download status report
-----------------------

If the client has attempted to download bytes for one or more DRS objects, a
download status report will be written to the output directory. This text file
includes a table, one row per downloaded file. Each row indicates whether the
file was successfully downloaded, and whether the file passed checksum 
validation (if validation was requested).

The columns of the download status report are as follows:

.. csv-table:: Download Status Report Columns
   :header: "Column #", "Field Name", "Description"
   :widths: 5 7 20

   "1", "ID", "ID of DRS object corresponding to downloaded file"
   "2", "Name", "Name of DRS object corresponding to downloaded file"
   "3", "Output File", "Local file where downloaded bytes were written"
   "4", "Download Status", "COMPLETED/FAILED. Indicates whether file was successfully downloaded"
   "5", "Checksum Status", "PASSED/FAILED. Indicates whether downloaded file passed checksum validation (if requested)"
   "6", "Hash Algorithm", "The hash algorithm used to perform checksum validation"
   "7", "Expected", "Digest value according to the DRS service/object metadata"
   "8", "Observed", "Digest value computed locally on the downloaded file"

