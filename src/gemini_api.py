# src/gemini_api.py
"""
Módulo para interação com a API do Google Gemini.

Responsabilidades:
- Configurar a API com a chave de acesso.
- Enviar prompts para o modelo generativo.
- Gerar respostas, hipóteses e sumarizações com base no contexto fornecido.
- Formatar as citações com base nos documentos recuperados.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

class GeminiAPI:
    """
    Encapsula a lógica de chamada à API do Gemini.
    """
    def __init__(self):
        """
        Carrega a chave da API e configura o modelo.
        """
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("A chave da API da Gemini não foi encontrada. Defina GEMINI_API_KEY no arquivo .env.")

        genai.configure(api_key=api_key)

        # Lógica para selecionar um modelo compatível dinamicamente
        model_name = 'models/gemini-1.5-pro-latest'
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if model_name not in available_models:
            # Se o preferido não estiver disponível, pega o primeiro 'gemini' compatível
            model_name = next((m for m in available_models if 'gemini' in m), None)

        if not model_name:
            raise ValueError("Nenhum modelo 'gemini' compatível com 'generateContent' foi encontrado.")

        print(f"Kosmos-Synesis usando o modelo: {model_name}")
        self.model = genai.GenerativeModel(model_name)

    def generate_response(self, query, context_docs):
        """
        Gera uma resposta aumentada por retrieval (RAG).

        Args:
            query (str): A pergunta do usuário.
            context_docs (list): Lista de documentos (chunks) recuperados do ChromaDB.

        Returns:
            str: A resposta gerada pelo modelo.
        """
        # Constrói o prompt com o contexto
        context_str = "\n\n".join(context_docs)
        prompt = f"""
        Com base nos seguintes trechos de artigos científicos, responda à pergunta.
        Se a resposta não estiver nos trechos, indique que a informação não foi encontrada.
        Sempre cite as fontes (metadados) dos trechos que você usar.

        Contexto:
        ---
        {context_str}
        ---

        Pergunta: {query}

        Resposta:
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Erro ao gerar resposta com a API da Gemini: {e}")
            return "Ocorreu um erro ao contatar a API da Gemini."

    def generate_hypothesis(self, topic, context_docs):
        """
        Gera uma nova hipótese de pesquisa com base em um tópico e contexto.
        """
        context_str = "\n\n".join(context_docs)
        prompt = f"""
        Você é um assistente de pesquisa criativo. Com base nos seguintes trechos
        de artigos sobre '{topic}', gere uma nova e interessante hipótese de pesquisa
        que conecte ou estenda as ideias apresentadas.

        Contexto:
        ---
        {context_str}
        ---

        Nova Hipótese de Pesquisa:
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Erro ao gerar hipótese com a API da Gemini: {e}")
            return "Ocorreu um erro ao gerar a hipótese."

if __name__ == '__main__':
    # Exemplo de uso simples (requer uma chave de API válida no .env)
    try:
        gemini = GeminiAPI()

        # Exemplo de chamada simples sem RAG
        simple_query = "Explique o conceito de 'attention mechanism' em 50 palavras."
        simple_response = gemini.model.generate_content(simple_query)
        print(f"Query: {simple_query}")
        print(f"Resposta da Gemini API:\n{simple_response.text}\n")

        # Exemplo de chamada com contexto (simulando RAG)
        rag_query = "O que é RAG e como funciona?"
        rag_context = [
            "Documento 1 (de Smith et al., 2020): Retrieval-Augmented Generation (RAG) é um método que combina um modelo de linguagem pré-treinado com um mecanismo de recuperação de informação. A ideia é fornecer ao modelo acesso a um corpo de conhecimento externo.",
            "Documento 2 (de Jones et al., 2021): O processo do RAG envolve duas etapas: primeiro, recuperar documentos relevantes de um grande corpus; segundo, usar esses documentos como contexto para um modelo generativo que produz a resposta final."
        ]
        rag_response = gemini.generate_response(rag_query, rag_context)
        print(f"Query RAG: {rag_query}")
        print(f"Resposta RAG da Gemini API:\n{rag_response}")

    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"Um erro inesperado ocorreu: {e}")
        print("Certifique-se de que sua chave GEMINI_API_KEY está configurada corretamente em um arquivo .env")
