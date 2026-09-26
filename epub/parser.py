import posixpath
import zipfile
import xml.etree.ElementTree as ET

from epub.metadata import parse_metadata
from epub.models import Book, Chapter, Metadata


class EPUBParser:
    def __init__(self, epub_path):
        self.epub_path = epub_path

    def parse(self):
        with zipfile.ZipFile(self.epub_path, "r") as epub:
            opf_path = self._find_opf_path(epub)
            opf_root = self._read_opf(epub, opf_path)

            metadata_data = parse_metadata(opf_root)

            metadata = Metadata(
                title=metadata_data["title"],
                author=metadata_data["author"],
                language=metadata_data["language"],
                identifier=metadata_data["identifier"],
            )

            chapters = self._parse_chapters(epub, opf_root, opf_path)

            cover = self._find_cover(epub, opf_root, opf_path)

            return Book(
                metadata=metadata,
                cover=cover,
                chapters=chapters,
                path=self.epub_path,
            )

    def _find_opf_path(self, epub):
        container_data = epub.read("META-INF/container.xml")
        container_root = ET.fromstring(container_data)

        namespace = {
            "container":
                "urn:oasis:names:tc:opendocument:xmlns:container"
        }

        rootfile = container_root.find(
            ".//container:rootfile",
            namespace,
        )

        if rootfile is None:
            raise ValueError("Could not find OPF file in EPUB.")

        return rootfile.attrib["full-path"]

    def _read_opf(self, epub, opf_path):
        opf_data = epub.read(opf_path)
        return ET.fromstring(opf_data)

    def _parse_chapters(self, epub, opf_root, opf_path):
        namespaces = {
            "opf": "http://www.idpf.org/2007/opf",
        }

        manifest = opf_root.find("opf:manifest", namespaces)
        spine = opf_root.find("opf:spine", namespaces)

        if manifest is None:
            raise ValueError("EPUB is missing a manifest.")

        if spine is None:
            raise ValueError("EPUB is missing a spine.")

        manifest_items = {}

        for item in manifest:
            manifest_items[item.attrib["id"]] = item.attrib

        chapters = []

        opf_directory = posixpath.dirname(opf_path)

        for index, itemref in enumerate(spine, start=1):
            idref = itemref.attrib["idref"]

            if idref not in manifest_items:
                continue

            item = manifest_items[idref]

            href = item["href"]
            media_type = item.get("media-type", "")

            if media_type not in (
                "application/xhtml+xml",
                "text/html",
            ):
                continue

            full_path = posixpath.normpath(
                posixpath.join(opf_directory, href)
            )

            content = epub.read(full_path).decode("utf-8", errors="replace")

            chapter = Chapter(
                title=f"Chapter {index}",
                href=full_path,
                content=content,
            )

            chapters.append(chapter)

        return chapters

    def _find_cover(self, epub, opf_root, opf_path):
        namespaces = {
            "opf": "http://www.idpf.org/2007/opf",
        }

        manifest = opf_root.find("opf:manifest", namespaces)

        if manifest is None:
            return None

        opf_directory = posixpath.dirname(opf_path)

        # EPUB 3: look for an item with properties="cover-image"
        for item in manifest:
            properties = item.attrib.get("properties", "")

            if "cover-image" in properties:
                href = item.attrib.get("href")

                if href:
                    return posixpath.normpath(
                        posixpath.join(opf_directory, href)
                    )

        # Older EPUBs: look for metadata pointing to a cover ID
        cover_meta = opf_root.find(
            ".//opf:meta[@name='cover']",
            namespaces,
        )

        if cover_meta is not None:
            cover_id = cover_meta.attrib.get("content")

            for item in manifest:
                if item.attrib.get("id") == cover_id:
                    href = item.attrib.get("href")

                    if href:
                        return posixpath.normpath(
                            posixpath.join(opf_directory, href)
                        )

        return None