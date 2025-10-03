# Kosmos-Synesis

Plataforma de pesquisa científica automatizada com RAG (Retrieval-Augmented Generation) para buscar, ler e interpretar artigos do arXiv. Gera resumos, cruza informações e propõe hipóteses com base na literatura analisada.

## Recursos

- **Busca automática**: Pesquisa artigos no arXiv por palavras‑chave.
- **Interpretação de texto**: Usa modelos de IA para entender conteúdo.
- **Sumarização**: Gera resumos concisos e informativos.
- **Síntese**: Conecta informações de múltiplas fontes.
- **Geração de hipóteses**: Propõe novas ideias com base nos trechos recuperados.

## Instalação

1. Crie e ative o ambiente virtual (Windows PowerShell):
   ```bash
   python -m venv .venv
   . .venv/\Scripts/Activate.ps1
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Crie o arquivo `.env` na raiz com sua chave:
   ```env
   GEMINI_API_KEY="sua_chave_aqui"
   ```
   Optional:
   ```env
   # CHROMADB_PATH="data/embeddings"
   # PAPERS_DATA_PATH="data/papers"
   # GEMINI_MODEL_NAME="models/gemini-1.5-pro-latest"
   ```

## Uso (Interface Web)

Para iniciar a aplicação principal (Streamlit):

```bash
streamlit run src/streamlit_app.py
```

## Uso Programático (para Devs)

O arquivo `src/gemini_api.py` contém um exemplo de uso da classe `GeminiAPI`:

```bash
python src/gemini_api.py
```

Demonstra:
- Instanciação de `GeminiAPI`;
- Chamada simples sem RAG;
- Chamada com contexto (simulado) estilo RAG.

## Exemplos

Veja também os notebooks em `notebooks/` para demonstrações adicionais.
