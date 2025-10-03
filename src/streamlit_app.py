# src/streamlit_app.py
"""
Interface web para o Kosmos-Synesis usando Streamlit.

Permite ao usuário:
- Inserir uma query de busca para o arXiv.
- Ver os resultados da busca.
- Selecionar papers para processamento.
- Fazer perguntas sobre os papers processados e ver as respostas do RAG.
- Gerar novas hipóteses de pesquisa.
"""

import streamlit as st
from arxiv_processor import ArxivProcessor
from rag_engine import RAGEngine
from gemini_api import GeminiAPI

# Inicialização dos componentes (pode ser otimizado com cache do Streamlit)
@st.cache_resource
def init_components():
    """Inicializa e retorna os componentes principais da aplicação."""
    st.write("Inicializando componentes... (isso só acontece uma vez)")
    arxiv_proc = ArxivProcessor()
    rag_eng = RAGEngine()
    try:
        gemini_api = GeminiAPI()
    except ValueError as e:
        st.error(f"Erro de inicialização: {e}")
        st.stop()
    return arxiv_proc, rag_eng, gemini_api

def run():
    """
    Executa a aplicação Streamlit.
    """
    st.set_page_config(page_title="Kosmos-Synesis", layout="wide")
    st.title("🌌 Kosmos-Synesis: RAG para Pesquisa Científica no arXiv")

    arxiv_proc, rag_eng, gemini_api = init_components()

    # --- Seção 1: Busca e Processamento de Papers ---
    st.header("1. Buscar e Processar Papers do arXiv")
    query = st.text_input("Termos de busca para o arXiv (ex: 'quantum computing')", "large language models")
    max_results = st.slider("Número máximo de papers para buscar", 1, 1000, 10)

    if st.button("Buscar no arXiv"):
        with st.spinner("Buscando e baixando papers..."):
            papers_meta = arxiv_proc.search_and_download(query, max_results)
            st.session_state.papers_meta = papers_meta

            if not papers_meta:
                st.warning("Nenhum paper encontrado ou erro no download.")
            else:
                st.success(f"{len(papers_meta)} papers baixados e prontos para indexação.")
                # Indexação automática após o download
                for paper in papers_meta:
                    text = arxiv_proc.extract_text_from_pdf(paper["filepath"])
                    if text:
                        # Simplificação: usando o texto inteiro como um único chunk
                        # Em um sistema real, o texto seria dividido em chunks menores
                        rag_eng.index_paper(
                            paper_id=paper["id"],
                            text_chunks=[text],
                            metadata_chunks=[{"paper_id": paper["id"], "title": paper["title"]}]
                        )
                st.info("Papers indexados no banco de dados vetorial.")


    if 'papers_meta' in st.session_state and st.session_state.papers_meta:
        st.subheader("Papers Encontrados:")
        for paper in st.session_state.papers_meta:
            with st.expander(f"**{paper['title']}**"):
                st.write(f"**ID:** {paper['id']}")
                st.write(f"**Autores:** {', '.join(paper['authors'])}")
                st.write(f"**Publicado:** {paper['published']}")
                st.write(f"**Resumo:** {paper['summary']}")


    # --- Seção 2: Query RAG e Geração de Hipóteses ---
    st.header("2. Interagir com os Papers Indexados")
    if 'papers_meta' in st.session_state and st.session_state.papers_meta:
        rag_query = st.text_input("Faça uma pergunta sobre os papers acima", "What are the main challenges of LLMs?")

        if st.button("Obter Resposta (RAG)"):
            with st.spinner("Buscando informações e gerando resposta..."):
                # 1. Retrieval
                retrieved_results = rag_eng.retrieve(rag_query, n_results=3)
                if not retrieved_results or not retrieved_results['documents'][0]:
                    st.warning("Não foi possível encontrar informações relevantes nos papers indexados.")
                else:
                    context_docs = retrieved_results['documents'][0]
                    # 2. Augmentation + Generation
                    response = gemini_api.generate_response(rag_query, context_docs)
                    st.markdown("### Resposta Gerada")
                    st.markdown(response)

        if st.button("Gerar Nova Hipótese"):
            with st.spinner("Gerando uma nova hipótese de pesquisa..."):
                # Modificação: Em vez de usar todos os documentos, recuperamos os mais relevantes para a query.
                # Isso evita exceder o limite de contexto do modelo.
                retrieved_results = rag_eng.retrieve(rag_query, n_results=100) # Aumentado para 100 por solicitação
                if not retrieved_results or not retrieved_results['documents'][0]:
                    st.warning("Não foi possível encontrar informações relevantes para gerar uma hipótese.")
                else:
                    context_docs = retrieved_results['documents'][0]
                    hypothesis = gemini_api.generate_hypothesis(rag_query, context_docs)
                    st.markdown("### Hipótese Gerada")
                    st.markdown(hypothesis)
    else:
        st.info("Busque e processe alguns papers primeiro para poder interagir com eles.")

if __name__ == "__main__":
    run()
