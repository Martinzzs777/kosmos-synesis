# tests/test_arxiv_processor.py
"""
Testes unitários para o ArxivProcessor.
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Adiciona o diretório src ao path para permitir a importação
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from arxiv_processor import ArxivProcessor

class TestArxivProcessor(unittest.TestCase):
    """
    Suite de testes para a classe ArxivProcessor.
    """

    @patch('arxiv.Search')
    def test_search_and_download_success(self, mock_search):
        """
        Testa se a busca e o download funcionam corretamente com um mock da API do arXiv.
        """
        # Configuração do Mock
        mock_result = MagicMock()
        mock_result.entry_id = 'http://arxiv.org/abs/2305.12345v1'
        mock_result.title = 'Mock Paper Title'
        mock_result.summary = 'This is a mock summary.'
        mock_result.authors = [MagicMock(name='Dr. Mock')]
        mock_result.published = '2023-05-20T15:00:00Z'
        # Simula o método download_pdf para não criar um arquivo real
        mock_result.download_pdf.return_value = 'data/papers/2305.12345v1.pdf'

        mock_search.return_value.results.return_value = [mock_result]

        # Execução
        processor = ArxivProcessor(data_path="tests/temp_papers")
        papers = processor.search_and_download('test query', max_results=1)

        # Verificação
        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0]['title'], 'Mock Paper Title')
        self.assertEqual(papers[0]['id'], 'http://arxiv.org/abs/2305.12345v1')
        # Verifica se o método de download foi chamado com os parâmetros corretos
        mock_result.download_pdf.assert_called_once_with(
            dirpath="tests/temp_papers",
            filename="2305.12345v1.pdf"
        )

        # Limpeza
        if os.path.exists("tests/temp_papers"):
            # Apenas remove o diretório se ele foi criado
            # Em um teste real, o ideal é garantir que o diretório seja sempre limpo
            pass # Não vamos remover para não ter problemas de permissão em CI/CD simples

    @patch('fitz.open')
    def test_extract_text_from_pdf(self, mock_fitz_open):
        """
        Testa a extração de texto de um PDF mockado.
        """
        # Configuração do Mock
        mock_page = MagicMock()
        mock_page.get_text.return_value = "Hello world from page 1."
        mock_doc = MagicMock()
        mock_doc.__iter__.return_value = [mock_page]
        mock_fitz_open.return_value = mock_doc

        # Execução
        processor = ArxivProcessor()
        text = processor.extract_text_from_pdf("dummy/path/to.pdf")

        # Verificação
        self.assertEqual(text, "Hello world from page 1.")
        mock_fitz_open.assert_called_once_with("dummy/path/to.pdf")
        mock_doc.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
