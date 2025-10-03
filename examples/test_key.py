# test_key.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

print("Iniciando teste de chave de API...")

# Carrega o arquivo .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERRO: A variável de ambiente GEMINI_API_KEY não foi encontrada.")
else:
    print("Chave encontrada no ambiente.")
    try:
        genai.configure(api_key=api_key)
        
        # --- LÓGICA DE SELEÇÃO DE MODELO ---
        print("Listando modelos disponíveis...")
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        print(f"Modelos encontrados que suportam 'generateContent': {available_models}")
        
        # Tenta usar um modelo Pro, se não, pega o primeiro da lista
        model_name = 'models/gemini-1.5-pro-latest' # Tentativa prioritária
        if model_name not in available_models:
            model_name = next((m for m in available_models if 'gemini' in m), None)

        if not model_name:
            raise ValueError("Nenhum modelo 'gemini' compatível encontrado.")

        print(f"Usando o modelo: {model_name}")
        model = genai.GenerativeModel(model_name)
        # --- FIM DA LÓGICA ---

        print("Configuração da API bem-sucedida. Tentando gerar conteúdo...")
        response = model.generate_content("Diga 'Olá, mundo!' em português.")
        
        print("\n--- SUCESSO! ---")
        print("Resposta da API:", response.text)
        print("Sua chave de API e configuração estão funcionando corretamente.")

    except Exception as e:
        print("\n--- FALHA! ---")
        print(f"Ocorreu um erro ao tentar usar a API: {e}")