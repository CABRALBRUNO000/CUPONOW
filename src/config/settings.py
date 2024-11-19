import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Chain Configurations
TEMPERATURE = 0.7
MODEL_NAME = "gpt-3.5-turbo"

# Cache Settings
CACHE_ENABLED = True
CACHE_TIMEOUT = 3600  # 1 hora

# Product Display Settings
MAX_PRODUCTS_DISPLAY = 5
DEFAULT_CURRENCY = "R$"

# API Endpoints (para quando tivermos a API de produtos)
PRODUCT_API_URL = os.getenv("PRODUCT_API_URL", "")
