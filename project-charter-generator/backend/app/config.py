import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Centralized configuration class. Reads values from environment variables.
    """

    # Azure OpenAI
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY")
    AZURE_API_VERSION = os.getenv("AZURE_API_VERSION")
    AZURE_EMBEDDING_DEPLOYMENT = os.getenv("AZURE_EMBEDDING_DEPLOYMENT")
    AZURE_CHAT_DEPLOYMENT = os.getenv("AZURE_CHAT_DEPLOYMENT")

    # Databricks
    DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
    DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN")
    DATABRICKS_JOB_ID = os.getenv("DATABRICKS_JOB_ID")

    MAX_TOKENS=os.getenv("MAX_TOKENS")
    TEMPERATURE=os.getenv("TEMPERATURE")

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    TOP_K = int(os.getenv("TOP_K", "3"))

    DATABRICKS_TIMEOUT=10
    DATABRICKS_MAX_RETRIES=3
    DATABRICKS_RETRY_DELAY=2

    AZURE_TIMEOUT=10
    AZURE_MAX_RETRIES=3
    AZURE_RETRY_DELAY=2

    ENTRA_TENANT_ID = os.getenv("ENTRA_TENANT_ID")    
    ENTRA_CLIENT_ID = os.getenv("ENTRA_CLIENT_ID") 
    ENTRA_AUTHORITY = f"https://login.microsoftonline.com/{ENTRA_TENANT_ID}/v2.0"
    ENTRA_JWKS_URL = f"https://login.microsoftonline.com/{ENTRA_TENANT_ID}/discovery/v2.0/keys"


    PROMPT_TEMPLATE =
        (
            "You are a helpful assistant.\n"
            "Use ONLY the context and questionnaire data to answer. If the answer isn't in the context, say you don't know.\n\n"
            "Context:\n{context}\n\n"
            "Questionnaire:\n{questionnaire}\n\n"
            "Question:\n{question}\n\n"
            "Answer:"
        )
