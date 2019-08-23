AUTHTOKEN=`gcloud auth print-access-token`

drs get \
    -d \
    -s \
    -o output \
    -m output/bundle_metadata.json \
    -l output/bundle_logs.txt \
    -V DEBUG \
    -t ${AUTHTOKEN} \
    ${URL} \
    ${OBJECT_ID}
