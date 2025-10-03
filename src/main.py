# src/main.py
"""
Ponto de entrada principal para o sistema Kosmos-Synesis.

Este script orquestra o fluxo de trabalho completo:
1. Inicia a interface do usuário com Streamlit.
2. Permite que o usuário interaja com o sistema para pesquisar e analisar papers.
"""

import streamlit_app

def main():
    """
    Função principal que inicia a aplicação Streamlit.
    """
    print("Iniciando Kosmos-Synesis...")
    streamlit_app.run()

if __name__ == "__main__":
    main()
