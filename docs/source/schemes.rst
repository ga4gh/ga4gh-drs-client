Supported Schemes
=================

According to the `DRS Specification <https://ga4gh.github.io/data-repository-service-schemas/docs/>`_,
object bytes can be downloaded by multiple access method types. The DRS client
supports byte download by different types, indicated by the *type* parameter
of *AccessMethod* objects in a *DRSObject's* *access_methods* array. These
access method types correspond to URI schemes. For each *DRSObject*, the
client will attempt to download object bytes by each supported scheme in
sequence, until the file has been successfully downloaded, or until all
download options have been exhausted without success.

Currently, the DRS client supports download by **2** URI schemes/access method
types:

.. csv-table:: ga4gh-drs-client supported schemes
   :header: "Scheme", "Description"
   :widths: 10 20

   "gs", "Google Cloud Storage"
   "https", "Hypertext Transfer Protocol Secure"
