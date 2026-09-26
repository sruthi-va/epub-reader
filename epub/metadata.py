import xml.etree.ElementTree as ET

NAMESPACES = {
    "opf": "http://www.idpf.org/2007/opf",
    "dc": "http://purl.org/dc/elements/1.1/",
}


def parse_metadata(opf_root):
    title = opf_root.find(".//dc:title", NAMESPACES)
    author = opf_root.find(".//dc:creator", NAMESPACES)
    language = opf_root.find(".//dc:language", NAMESPACES)
    identifier = opf_root.find(".//dc:identifier", NAMESPACES)

    return {
        "title": title.text if title is not None else "",
        "author": author.text if author is not None else "",
        "language": language.text if language is not None else "",
        "identifier": identifier.text if identifier is not None else "",
    }