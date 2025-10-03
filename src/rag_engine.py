# src/rag_engine.py
"""
Módulo do motor RAG (Retrieval-Augmented Generation).

Responsabilidades:
- Gerar embeddings para o texto dos papers usando um modelo apropriado.
- Indexar os embeddings em um banco de dados vetorial (ChromaDB).
- Realizar buscas de similaridade para encontrar os trechos mais relevantes
  para uma dada query.
"""

import chromadb
from chromadb.utils import embedding_functions
import os

class RAGEngine:
    """
    Gerencia a indexação e retrieval de documentos.
    """
    def __init__(self, embedding_model_name="all-MiniLM-L6-v2", db_path="data/embeddings"):
        """
        Inicializa o motor RAG.

        Args:
            embedding_model_name (str): Nome do modelo de embedding a ser usado.
                                        Pode ser um modelo do sentence-transformers ou
                                        integrado com a API da Gemini no futuro.
            db_path (str): Caminho para o armazenamento do ChromaDB.
        """
        if not os.path.exists(db_path):
            os.makedirs(db_path)

        self.client = chromadb.PersistentClient(path=db_path)
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=embedding_model_name
        )
        self.collection = self.client.get_or_create_collection(
            name="arxiv_papers",
            embedding_function=self.embedding_function
        )

    def index_paper(self, paper_id, text_chunks, metadata_chunks):
        """
        Indexa os chunks de texto de um paper.

        Args:
            paper_id (str): Identificador único do paper.
            text_chunks (list): Lista de trechos de texto do paper.
            metadata_chunks (list): Lista de metadados correspondentes a cada chunk.
        """
        if not text_chunks:
            print(f"Nenhum chunk de texto para indexar para o paper {paper_id}.")
            return

        # Gera IDs únicos para cada chunk
        chunk_ids = [f"{paper_id}_{i}" for i in range(len(text_chunks))]

        try:
            self.collection.add(
                documents=text_chunks,
                metadatas=metadata_chunks,
                ids=chunk_ids
            )
            print(f"Paper {paper_id} indexado com {len(text_chunks)} chunks.")
        except Exception as e:
            print(f"Erro ao indexar o paper {paper_id}: {e}")

    def retrieve(self, query, n_results=5):
        """
        Busca os chunks mais relevantes para uma query.

        Args:
            query (str): A pergunta ou termo de busca.
            n_results (int): Número de resultados a serem retornados.

        Returns:
            dict: Dicionário com os resultados da busca.
        """
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            return results
        except Exception as e:
            print(f"Erro durante a busca: {e}")
            return None

if __name__ == '__main__':
    # Exemplo de uso
    rag = RAGEngine()

    # Exemplo de chunks (em um cenário real, viriam do arxiv_processor)
    paper_id_ex = "2305.12345"
    chunks_ex = [
        "Large language models (LLMs) are a type of artificial intelligence.",
        "Retrieval-Augmented Generation combines LLMs with external knowledge.",
        "This paper explores the application of RAG to scientific literature."
    ]
    metadatas_ex = [
        {"source": "title_section", "paper_id": paper_id_ex},
        {"source": "intro_section", "paper_id": paper_id_ex},
        {"source": "conclusion_section", "paper_id": paper_id_ex}
    ]

    rag.index_paper(paper_id_ex, chunks_ex, metadatas_ex)

    query_ex = "What is RAG?"
    retrieved_docs = rag.retrieve(query_ex)

    if retrieved_docs:
        print(f"\nResultados para a query: '{query_ex}'")
        for i, doc in enumerate(retrieved_docs['documents'][0]):
            print(f"  {i+1}. {doc}")
            print(f"     Metadata: {retrieved_docs['metadatas'][0][i]}")
