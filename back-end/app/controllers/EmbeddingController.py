from bs4 import BeautifulSoup


class EmbeddingController:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def html_to_docs(self, url):
        doc = BeautifulSoup(url, "html.parser")
        return doc.get_text()

    async def embedding(self, embedding_request):
        pass

