import os
import json
from typing import Dict, List
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

load_dotenv()  # Carrega as variáveis de ambiente do arquivo .env

class AIService:
    def __init__(self):
        openai_api_key = os.getenv("OPENAI_API_KEY")  # Obtém a chave de API da variável de ambiente
        self.llm = ChatOpenAI(openai_api_key=openai_api_key)  # Passa a chave de API ao criar a instância do ChatOpenAI   
        
    def get_system_prompt(self):
        return SystemMessage(content="""
    Você é um assistente especializado em encontrar e recomendar cupons de desconto.
    Para cada produto mencionado, você DEVE retornar uma resposta no seguinte formato JSON:
    {
        "message": "sua mensagem amigável para o usuário",
        "products": [
            {
                "name": "Nome do Produto",
                "original_price": 1999.99,
                "discount": 15,
                "coupon": "CODIGO15",
                "link": "https://exemplo.com/produto",
                "image": "https://exemplo.com/imagem.jpg"
            }
        ]
    }
    Sempre inclua todos os campos necessários para cada produto.
    Mantenha este formato JSON para garantir que os produtos sejam exibidos corretamente.
    """)
    
    async def get_response(self, user_message: str, chat_history: list = None):
        if chat_history is None:
            chat_history = []        
        messages = [self.get_system_prompt()]
    
        # Converte histórico do chat
        for msg in chat_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))
            
        messages.append(HumanMessage(content=user_message))
    
        # Obtém resposta do modelo
        response = await self.llm.agenerate([messages])
    
        try:
            # Tenta fazer o parse do JSON
            return json.loads(response.generations[0][0].text)
        except json.JSONDecodeError:
            # Retorna um formato válido mesmo em caso de erro
            return {
                "message": response.generations[0][0].text,
                "products": []
            }