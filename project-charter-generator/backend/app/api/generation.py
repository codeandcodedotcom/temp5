from flask import Blueprint, request, jsonify
from app.services import azure_openai, databricks, prompt_builder
from app.config import Config
from app.utils.logger import get_logger
from app.utils.jwt_auth import require_jwt


bp = Blueprint("generation", __name__)
logger = get_logger(__name__)

@bp.route("/ask", methods=["POST"])
@require_jwt
def ask():
    """
    Orchestrates: user input -> embedding -> Databricks retrieval -> prompt -> Azure LLM -> response.
    """
    data = request.json or {}
    query = data.get("query", "").strip()
    if not query:
        logger.warning("Missing 'query' in request body")
        return jsonify({"error": "Missing 'query'"}), 400

    # questionnaire = (data.get("questionnaires") or "").strip()
    top_k       = int(data.get("top_k") or Config.TOP_K)
    # max_tokens  = int(data.get("max_tokens") or Config.MAX_TOKENS)
    # temperature = float(data.get("temperature") or Config.TEMPERATURE)

    logger.info(
        f"Orchestration start (len(query)={len(query)}, top_k={top_k}, "
        f"max_tokens={max_tokens}, temperature={temperature})"
    )

    # 1) Embed user query
    embedding = azure_openai.embed_text(query)

    # 2) Retrieve context from Databricks (vector search over stored data)
    docs = databricks.retrieve_context(embedding, top_k=top_k)

    # 3) Build prompt from context + query
    prompt = prompt_builder.build_prompt(query, docs, questionnaire)

    # 4) Generate answer with Azure OpenAI
    answer = azure_openai.generate_answer(
        prompt=prompt,
        # max_tokens=max_tokens,
        # temperature=temperature
    )

    logger.info(f"Orchestration success (answer_chars={len(answer)}, docs={len(docs)})")

    # 5) Return JSON
    return jsonify({
        "answer": answer,
        "used_top_k": top_k,
        "docs_count": len(docs),
        # "context_preview": prompt[:800]
    })
