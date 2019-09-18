# Change Log

## version 0.1.6 - 2019-09-18

* prevent downloaded file name collisions by making the write path: ${DATADIR}/${OBJID}/${FILENAME}
* command-line args, logger, exit code are now part of global state object

## version 0.1.5 - 2019-09-17

* added method to download object bytes when `access_id` is provided instead of `access_url`
* added failure exit codes when not all files were successfully downloaded/passed checksum validation

## version 0.1.4 - 2019-09-05

* fixed entrypoint help messages

## version 0.1.3 - 2019-09-04

* added "schemes ls" entrypoint
* added documentation on supported uri schemes

## version 0.1.2 - 2019-09-03

* added command-line validation
* check output directories exist, handle invalid urls, unrecognized hosts

## version 0.1.1 - 2019-08-30

* added bundle download functionality and threaded downloading

## version 0.1.0 - 2019-08-19

* initial development version
