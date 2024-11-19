import streamlit as st
import asyncio
from services.ai_service import AIService

# Page Configuration
st.set_page_config(
    page_title="Cuponow",
    page_icon="🏷️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# [Previous CSS styles remain the same]
st.markdown("""
    <style>
            
        /* Hide Streamlit elements */
        MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Improved base styles */
        .stApp {
            background-color: #F8FAFC;
        }
        /* Custom component styles */
        .card {
            border-radius: 12px;
            padding: 1rem;
            border: 1px solid #E2E8F0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.02);
            margin-bottom: 1.5rem;
        }
        
        .product-card {
            border-radius: 12px;
            border: 1px solid #E2E8F0;
            transition: all 0.3s ease;
            height: 100%;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            margin-bottom: 1.5rem;
        }
        
        .product-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 12px 24px rgba(0,0,0,0.08);
        }
        
        .custom-button {
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            border: none;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        
        .custom-button:hover {
            transform: translateY(-1px);
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div style="text-align: center; padding: 3rem 0;margin-top: -150px;">
        <h1 style="font-size: 3rem; margin-bottom: 1rem; background: linear-gradient(90deg, #3B82F6, #2563EB); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Cuponow</h1>
        <p style="color: #64748B; font-size: 1.2rem; max-width: 600px; margin: 0 auto;">Encontre as melhores ofertas de forma inteligente com nossa IA</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="card">
        <div style="display: flex; align-items: start; gap: 2rem;">
            <div style="flex: 2;">
                <h2 style="color: #2563EB; margin-bottom: 1rem;">Descubra Ofertas Inteligentes</h2>
                <p style="color: #64748B; font-size: 1.1rem; line-height: 1.6; margin-bottom: 1rem;">
                    O Cuponow utiliza inteligência artificial para encontrar as melhores ofertas baseadas nas suas preferências. 
                    Nossa tecnologia analisa milhares de produtos em tempo real para trazer descontos exclusivos.
                </p>
                <div style="display: flex; gap: 1rem; margin-top: 1.5rem;">
                    <div style="background: #EFF6FF; padding: 1rem; border-radius: 8px; flex: 1;">
                        <h4 style="color: #2563EB; margin-bottom: 0.5rem;">Ofertas Personalizadas</h4>
                        <p style="color: #64748B; font-size: 0.9rem;">Recomendações baseadas no seu perfil</p>
                    </div>
                    <div style="background: #EFF6FF; padding: 1rem; border-radius: 8px; flex: 1;">
                        <h4 style="color: #2563EB; margin-bottom: 0.5rem;">Economia Real</h4>
                        <p style="color: #64748B; font-size: 0.9rem;">Cupons verificados e atualizados</p>
                    </div>
                </div>
            </div>
            <div style="flex: 1; background: linear-gradient(135deg, #3B82F6, #2563EB); padding: 2rem; border-radius: 12px; color: white;">
                <h3 style="margin-bottom: 1rem;">Destaques</h3>
                <ul style="list-style: none; padding: 0;">
                    <li style="margin-bottom: 0.5rem;">✨ Cashback em todas compras</li>
                    <li style="margin-bottom: 0.5rem;">🔥 Ofertas exclusivas</li>
                    <li style="margin-bottom: 0.5rem;">🎯 Cupons verificados</li>
                    <li>⚡ Alertas de preço</li>
                </ul>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Initialize AI Service
@st.cache_resource
def get_ai_service():
    return AIService()

ai_service = get_ai_service()

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "products" not in st.session_state:
    st.session_state.products = []


# Main content
products_col, chat_col = st.columns([7, 3])
# Products Column
with products_col:
    st.markdown("""
        <div class="card">
            <h2 style="margin-bottom: 1rem;">Produtos em Destaque</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.products:
        st.info("Inicie uma conversa com o assistente para descobrir ofertas!")
    else:
        # Create rows dynamically based on number of products
        products_per_row = 3
        for i in range(0, len(st.session_state.products), products_per_row):
            cols = st.columns(products_per_row)
            for j in range(products_per_row):
                idx = i + j
                if idx < len(st.session_state.products):
                    product = st.session_state.products[idx]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="product-card">
                                <img src="{product['image']}" style="width: 100%; height: 200px; object-fit: cover; border-radius: 8px 8px 0 0;">
                                <div style="padding: 1rem;">
                                    <div style="color: #2563EB; font-size: 0.875rem; margin-bottom: 0.5rem;">
                                        {product['discount']}% OFF
                                    </div>
                                    <h3 style="font-size: 1rem; margin-bottom: 0.5rem;">{product['name']}</h3>
                                    <div style="display: flex; align-items: baseline; gap: 0.5rem; margin-bottom: 1rem;">
                                        <span style="font-size: 1.25rem; font-weight: 600;">
                                            R$ {product['original_price'] * (1 - product['discount']/100):.2f}
                                        </span>
                                        <span style="color: #64748B; text-decoration: line-through;">
                                            R$ {product['original_price']:.2f}
                                        </span>
                                    </div>
                                    <a href="{product['link']}" target="_blank" style="text-decoration: none;">
                                        <button class="custom-button" style="width: 100%;">
                                            Ver oferta
                                        </button>
                                    </a>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

# Chat Column
with chat_col:
    st.markdown("""
        <div class="card">
            <h2 style="text-align: center; margin-bottom: 1rem;">Assistente Virtual</h2>
        </div>
    """, unsafe_allow_html=True)
    
    chat_container = st.container()
    
    with chat_container:
        input_container = st.container()
        messages_container = st.container()
        
        with input_container:
            prompt = st.chat_input("Como posso ajudar você hoje?")
            if prompt:
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                try:
                    response = asyncio.run(ai_service.get_response(
                        prompt,
                        st.session_state.messages[:-1]
                    ))
                    
                    # Handle products - now prepending new products
                    if "products" in response and response["products"]:
                        new_products = []
                        for new_product in response["products"]:
                            if not any(p.get("name") == new_product["name"] for p in st.session_state.products):
                                new_products.append(new_product)
                        
                        # Prepend new products to the existing list
                        st.session_state.products = new_products + st.session_state.products
                    
                    st.session_state.messages.append({"role": "assistant", "content": response["message"]})
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao processar a resposta: {str(e)}")
        
        with messages_container:
            for message in reversed(st.session_state.messages):
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])