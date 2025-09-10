from flask import Blueprint, request, jsonify
from app.services import azure_openai, databricks, prompt_builder
from app.config import Config
from app.utils.logger import get_logger
from app.utils.jwt_auth import require_jwt


bp = Blueprint("generation", __name__)
logger = get_logger(__name__)

# @bp.route("/ask", methods=["POST"])
# # @require_jwt
# def ask():
#     """
#     Orchestrates: user input -> embedding -> Databricks retrieval -> prompt -> Azure LLM -> response.
#     """
#     data = request.json or {}
#     query = data.get("query", "").strip()
#     if not query:
#         logger.warning("Missing 'query' in request body")
#         return jsonify({"error": "Missing 'query'"}), 400

#     # questionnaire = (data.get("questionnaires") or "").strip()
#     top_k       = int(data.get("top_k") or Config.TOP_K)
#     # max_tokens  = int(data.get("max_tokens") or Config.MAX_TOKENS)
#     # temperature = float(data.get("temperature") or Config.TEMPERATURE)

#     logger.info(
#         f"Orchestration start (len(query)={len(query)}, top_k={top_k}, "
#         f"max_tokens={max_tokens}, temperature={temperature})"
#     )

#     # 1) Embed user query
#     embedding = azure_openai.embed_text(query)

#     # 2) Retrieve context from Databricks (vector search over stored data)
#     docs = databricks.retrieve_context(embedding, top_k=top_k)

#     # 3) Build prompt from context + query
#     prompt = prompt_builder.build_prompt(query, docs, questionnaire)

#     # 4) Generate answer with Azure OpenAI
#     answer = azure_openai.generate_answer(
#         prompt=prompt,
#         # max_tokens=max_tokens,
#         # temperature=temperature
#     )

#     logger.info(f"Orchestration success (answer_chars={len(answer)}, docs={len(docs)})")

#     # 5) Return JSON
#     return jsonify({
#         "answer": answer,
#         "used_top_k": top_k,
#         "docs_count": len(docs),
#         # "context_preview": prompt[:800]
#     })



        resp = {
            "project_title": parsed.get("project_title", data.get("project_name", "Untitled Project")),
            "project_description": parsed.get("project_description", parsed.get("description", llm_text)),
            "project_budget": parsed.get("project_budget", "Estimated TBD"),
            "complexity_score": parsed.get("complexity_score", 3),
            "recommended_pm_count": parsed.get("recommended_pm_count", 1),
            "rationale": parsed.get("rationale", ""),
            "key_risks": parsed.get("key_risks", []),
            "supporting_documents": docs,
            "diagnostics": {
                "submission_id": submission_id,
                "used_top_k": int(getattr(Config, "TOP_K", 3)),
                "embedding_time_ms": embed_ms,
                "retrieval_time_ms": retrieval_ms,
                "generation_time_ms": generation_ms
            },
            "raw_llm_output": llm_text
        }
        return jsonify(resp), 200

    if submission_id:
        try:
            storage.save_result(submission_id, response)
        except Exception:
            current_app.logger.exception("Failed to save result")

    except Exception as exc:
        logger.exception("Error in /api/generation/ask")
        return jsonify({"error": "Internal Server Error"}), 500


@bp.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    answers = data.get("answers", [])

    if not answers:
        return jsonify({"error": "Missing field 'answers'"}), 400

    # Build query text from answers
    query_text = " ".join([a.get("answer", "") for a in answers])

    # For now, return dummy response
    dummy_response = {
        "project_title": data.get("project_name", "Untitled Project"),
        "project_description": f"Generated description based on answers: {query_text}",
        "project_budget": "Estimated TBD",
        "complexity_score": 3,
        "recommended_pm_count": 1,
        "rationale": "Demo response",
        "key_risks": ["Demo risk 1", "Demo risk 2"],
        "supporting_documents": [],
        "diagnostics": {"used_top_k": 0}
    }

    return jsonify(dummy_response), 200


