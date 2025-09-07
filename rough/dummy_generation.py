from flask import Blueprint, request, jsonify, current_app

bp = Blueprint("generation", __name__)

@bp.route("/ask", methods=["POST"])
def ask():
    """
    Dummy implementation of the /ask route.
    Accepts a request JSON and returns a static dummy response
    in the agreed schema so frontend can integrate.
    """
    data = request.get_json(silent=True)

    if not data or "answers" not in data:
        return jsonify({"error": "Missing field 'answers'"}), 400

    current_app.logger.info("Received dummy /ask request", extra={"data": data})

    # Hardcoded dummy response
    dummy_response = {
        "project_title": "CRM Upgrade Initiative",
        "project_description": "Migration of legacy CRM to Salesforce to improve scalability and customer data management.",
        "project_budget": "Estimated 50 million USD",
        "complexity_score": 3,
        "recommended_pm_count": 2,
        "rationale": "Cross-department dependencies and integration complexity justify score 3.",
        "key_risks": [
            "Data migration challenges",
            "Integration delays"
        ],
        "supporting_documents": [
            {
                "id": "doc-001",
                "source": "Policies/Procurement.pdf",
                "excerpt": "Procurement approval required for >$1M",
                "score": 0.95
            }
        ],
        "diagnostics": {
            "used_top_k": 3,
            "retrieval_time_ms": 120,
            "generation_time_ms": 890
        }
    }

    return jsonify(dummy_response), 200







# curl -X POST http://localhost:5000/api/generation/ask \
#   -H "Content-Type: application/json" \
#   -d '{
#     "project_name": "CRM Upgrade Initiative",
#     "sponsor": "Alice Smith",
#     "answers": [
#       {"id": "q1", "question": "Do you have budget?", "answer": "Yes"}
#     ]
#   }'
