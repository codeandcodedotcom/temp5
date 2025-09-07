from typing import List, Dict
from app.config import Config
from app.utils.logger import get_logger

logger = get_logger(__name__)

def build_context_block(docs: List[Dict]) -> str:
    """
    Join retrieved docs into a single context block.
    """
    parts = []
    for i, d in enumerate(docs, start=1):
        text = d.get("content") or d.get("text") or ""
        if not text:
            logger.warning(f"Document {i} missing 'content'/'text' field")
        parts.append(f"{i}. {text}".strip())
    ctx = "\n".join(p for p in parts if p)
    logger.info(f"Built context block with {len(parts)} segments")
    return ctx

def build_prompt(question: str, docs: List[Dict], instructions: str = "") -> str:
    """
    Fill the configurable template with context, question, and optional instructions.
    """
    context_block = build_context_block(docs)
    prompt = Config.PROMPT_TEMPLATE.format(
        context=context_block,
        question=question,
        questionnaire=questionnaire or "Follow formatting exactly and be concise."
    )
    logger.info(f"Prompt built (context_chars={len(context_block)}, question_chars={len(question)})")
    return prompt
