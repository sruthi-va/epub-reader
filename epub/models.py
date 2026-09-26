class Metadata:
    def __init__(self, title="", author="", language="", identifier=""):
        self.title = title
        self.author = author
        self.language = language
        self.identifier = identifier


class Chapter:
    def __init__(self, title="", href="", content=""):
        self.title = title
        self.href = href
        self.content = content


class Book:
    def __init__(
        self,
        metadata=None,
        cover=None,
        chapters=None,
        path=None,
    ):
        self.metadata = metadata or Metadata()
        self.cover = cover
        self.chapters = chapters or []
        self.path = path

    @property
    def title(self):
        return self.metadata.title

    @property
    def author(self):
        return self.metadata.author

    @property
    def language(self):
        return self.metadata.language

    @property
    def identifier(self):
        return self.metadata.identifier