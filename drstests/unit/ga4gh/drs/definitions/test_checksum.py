from ga4gh.drs.definitions.checksum import Checksum

data = [
    {
        "checksum": "3332ed720ac7eaa9b3655c06f6b9e196",
        "type": "md5"
    },

    {
        "checksum": "959cb1883fc1ca9ae1394ceb475a356ead1ecceff5824ae7",
        "type": "sha512"
    },

    {
        "checksum": "b7ebc601f9a7df2e1ec5863deeae88a3",
        "type": "md5"
    }

]

def test_checksum():

    for json in data:
        c = Checksum(json)
        assert c.checksum == json["checksum"]
        assert c.type == json["type"]