import os
import httpx
from openai import AzureOpenAI
from app.config import Config
from app.utils.logger import get_logger

logger = get_logger(__name__)

REQUEST_TIMEOUT = int(Config.AZURE_TIMEOUT or 10) 
MAX_RETRIES = int(Config.AZURE_MAX_RETRIES or 3)  
RETRY_DELAY = int(Config.AZURE_RETRY_DELAY or 2) 

http_client = httpx.Client(timeout=REQUEST_TIMEOUT)

client = AzureOpenAI(
    azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
    api_key=Config.AZURE_OPENAI_KEY,
    api_version=Config.AZURE_API_VERSION,
    http_client=http_client
)

EMBEDDING_DEPLOYMENT = Config.AZURE_EMBEDDING_DEPLOYMENT
CHAT_DEPLOYMENT = Config.AZURE_CHAT_DEPLOYMENT   


def _with_retry(func, *args, **kwargs):
    """
    Call func(*args, **kwargs) with retries + timeout.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info(f"Azure API call {func.__name__} attempt={attempt}/{MAX_RETRIES}")
            return func(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Azure API call failed on attempt {attempt}: {e}", exc_info=True)
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                logger.error(f"Azure API call failed after {MAX_RETRIES} attempts")
                raise



def embed_text(text: str):
    """
    Create embeddings for input text using Azure OpenAI embedding model.
    """
    response = _with_retry(
        client.embeddings.create,
        model=EMBEDDING_DEPLOYMENT,
        input=text,
    )
    embedding = response.data[0].embedding
    logger.info(f"Generated embedding (len={len(embedding)}) for text length={len(text)}")
    return embedding


def generate_answer(prompt: str):
    """
    Generate answer using Azure OpenAI chat model.
    """
    response = _with_retry(
        client.chat.completions.create,
        model=Config.AZURE_CHAT_DEPLOYMENT,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=Config.MAX_TOKENS,
        temperature=Config.TEMPERATURE
    )
    answer = response.choices[0].message.content
    logger.info(f"LLM response generated successfully (length={len(answer)})")
    return answer

