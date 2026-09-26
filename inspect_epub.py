import zipfile
import xml.etree.ElementTree as ET

epub_path = r"C:\Users\sruth\Downloads\Monstrilio _ A Novel -- Gerardo Sámano Córdova -- Lightning Source Inc_ (Tier 1), New York, 2023 -- Zando -- isbn13 9781638930365 -- d1f9be176ea6d5e22e95510a0a3884fa -- Anna’s Archive.epub"


def main():

    print("=" * 40)
    print("EPUB INSPECTOR")
    print("=" * 40)

    with zipfile.ZipFile(epub_path) as epub:

        # --------------------------------
        # Archive
        # --------------------------------

        print("\nArchive contents:\n")

        for filename in epub.namelist():
            print(f"  {filename}")

        # --------------------------------
        # Container
        # --------------------------------

        container_data = epub.read(
            "META-INF/container.xml"
        )

        container_root = ET.fromstring(
            container_data
        )

        container_namespaces = {
            "container":
                "urn:oasis:names:tc:opendocument:xmlns:container"
        }

        rootfile = container_root.find(
            ".//container:rootfile",
            container_namespaces,
        )

        opf_path = rootfile.attrib["full-path"]

        print("\n" + "-" * 40)
        print("PACKAGE")
        print("-" * 40)

        print(f"\nOPF: {opf_path}")

        # --------------------------------
        # OPF
        # --------------------------------

        opf_data = epub.read(opf_path)

        opf_root = ET.fromstring(opf_data)

        namespaces = {
            "opf": "http://www.idpf.org/2007/opf",
            "dc": "http://purl.org/dc/elements/1.1/",
        }

        # --------------------------------
        # Metadata
        # --------------------------------

        title = opf_root.find(
            ".//dc:title",
            namespaces
        )

        creator = opf_root.find(
            ".//dc:creator",
            namespaces
        )

        language = opf_root.find(
            ".//dc:language",
            namespaces
        )

        print("\n" + "-" * 40)
        print("METADATA")
        print("-" * 40)

        print(
            "\nTitle:",
            title.text if title is not None else "Unknown"
        )

        print(
            "Author:",
            creator.text if creator is not None else "Unknown"
        )

        print(
            "Language:",
            language.text if language is not None else "Unknown"
        )

        # --------------------------------
        # Manifest
        # --------------------------------

        manifest = opf_root.find(
            "opf:manifest",
            namespaces
        )

        manifest_items = {}

        for item in manifest:
            manifest_items[item.attrib["id"]] = item.attrib

        # --------------------------------
        # Spine
        # --------------------------------

        spine = opf_root.find(
            "opf:spine",
            namespaces
        )

        print("\n" + "-" * 40)
        print("CHAPTERS")
        print("-" * 40)

        for index, itemref in enumerate(
            spine,
            start=1
        ):

            idref = itemref.attrib["idref"]

            item = manifest_items[idref]

            print(
                f"{index}. {item['href']}"
            )


if __name__ == "__main__":
    main()