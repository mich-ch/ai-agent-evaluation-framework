import os
from dotenv import load_dotenv

# Φορτώνει το API key από το .env αρχείο
load_dotenv()

# Ορίζουμε το βασικό μονοπάτι του project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Το μονοπάτι για το αρχείο δεδομένων
DATA_PATH = os.path.join(BASE_DIR, 'data', 'Store_Sales_Price_Elasticity_Promotions_Data.parquet')

# Ρυθμίσεις Μοντέλου
MODEL_NAME = "gpt-4o-mini"
PHOENIX_PROJECT_NAME = "ai-agent-evaluation-v1"