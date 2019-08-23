AUTHTOKEN=`gcloud auth print-access-token`

drs get \
    -d \
    -s \
    -o output \
    -m output/object_metadata.json \
    -l output/object_logs.txt \
    -V DEBUG \
    -t ${AUTHTOKEN} \
    ${URL} \
    ${OBJECT_ID}
