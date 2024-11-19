import pytest
from services.ai_service import AIService

pytestmark = pytest.mark.asyncio

@pytest.mark.asyncio
async def test_ai_service():
    ai = AIService()
    response, products = await ai.get_response("Procuro cupom de celular")
    print("Resposta:", response)
    print("Produtos:", products)

    # Teste com cache
    cached_response, cached_products = await ai.get_response("Procuro cupom de celular")
    print("\nResposta do cache:", cached_response)

    # Teste de personalização
    personalized_response = await ai.personalization_chain.apredict(
        history="Usuário sempre procura eletrônicos",
        products=str(products)
    )
    print("\nResposta personalizada:", personalized_response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_ai_service())
