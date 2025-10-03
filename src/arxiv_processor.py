# src/arxiv_processor.py
"""
Módulo responsável por interagir com a API do arXiv e processar os papers.

Funcionalidades:
- Buscar artigos no arXiv por palavra-chave.
- Baixar o PDF do artigo.
- Extrair texto e metadados do PDF usando PyMuPDF.
- Salvar o conteúdo processado para uso posterior.
"""

import arxiv
import fitz  # PyMuPDF
import os

class ArxivProcessor:
    """
    Processa papers do arXiv, desde a busca até a extração de texto.
    """
    def __init__(self, data_path="data/papers"):
        self.data_path = data_path
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

    def search_and_download(self, query, max_results=1000):
        """
        Busca papers no arXiv e baixa os PDFs.
        Retorna uma lista de metadados dos papers baixados.
        """
        # Expandido de 5 para 1000 papers por busca.
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )

        downloaded_papers = []
        for result in search.results():
            try:
                filename = f"{result.entry_id.split('/')[-1]}.pdf"
                filepath = os.path.join(self.data_path, filename)
                result.download_pdf(dirpath=self.data_path, filename=filename)
                print(f"Paper '{result.title.encode('ascii', 'ignore').decode('ascii')}' baixado em: {filepath}")
                downloaded_papers.append({
                    "id": result.entry_id,
                    "title": result.title,
                    "summary": result.summary,
                    "authors": [author.name for author in result.authors],
                    "published": result.published,
                    "filepath": filepath
                })
            except Exception as e:
                print(f"Erro ao baixar o paper '{result.title.encode('ascii', 'ignore').decode('ascii')}': {e}")
        return downloaded_papers

    def extract_text_from_pdf(self, filepath):
        """
        Extrai o texto de um arquivo PDF.
        """
        try:
            doc = fitz.open(filepath)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            print(f"Erro ao extrair texto de '{filepath}': {e}")
            return None

if __name__ == '__main__':
    # Exemplo de uso
    processor = ArxivProcessor()
    papers_meta = processor.search_and_download("Large Language Models", max_results=2)
    if papers_meta:
        first_paper_path = papers_meta[0]["filepath"]
        text = processor.extract_text_from_pdf(first_paper_path)
        if text:
            print(f"\nTexto extraído do paper '{papers_meta[0]['title'].encode('ascii', 'ignore').decode('ascii')}':")
            print(text[:500] + "...")
