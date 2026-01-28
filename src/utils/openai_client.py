import os
from openai import OpenAI

def get_openai_client():
    """Επιστρέφει ένα έτοιμο OpenAI client χρησιμοποιώντας το κλειδί από το περιβάλλον."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found. Βεβαιώσου ότι έχεις φτιάξει το αρχείο .env")
    return OpenAI(api_key=api_key)