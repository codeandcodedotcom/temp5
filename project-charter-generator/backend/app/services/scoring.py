from typing import Dict
from app.utils.logger import get_logger

logger = get_logger(__name__)

def interpret_score(total_score: int) -> Dict[str, str]:
    """
    Interpret total_score and return complexity description + recommendation.
    (Exactly the logic you provided.)
    """
    try:
        total_score = int(total_score)
    except Exception:
        logger.warning("interpret_score: invalid total_score %r", total_score)
        return {"complexity": "Invalid Score", "recommendation": "Score out of expected range."}

    if 1 <= total_score <= 27:
        return {
            "complexity": "Low Complexity / Standard execution",
            "recommendation": (
                "At this stage, the project does not require the support of a dedicated "
                "Project Management (PM) professional. Please reach out to your division PMO "
                "for guidance, support, and training recommendations as needed."
            ),
        }
    elif 28 <= total_score <= 39:
        return {
            "complexity": "Medium Complexity / Focus on risk",
            "recommendation": (
                "Based on the assessment, this project could be assigned a Project Lead. "
                "A Project Lead could provide the necessary oversight and direction to ensure successful delivery."
            ),
        }
    elif 40 <= total_score <= 51:
        return {
            "complexity": "High Complexity / Need active governance",
            "recommendation": (
                "The assessment indicates that this project should be managed by a Project Manager. "
                "Assigning a Project Manager will help ensure effective planning, execution, and control "
                "throughout the project lifecycle."
            ),
        }
    elif 52 <= total_score <= 60:
        return {
            "complexity": "Critical Complexity / Need active governance",
            "recommendation": (
                "The assessment suggests that this initiative is best classified as a Programme. "
                "It should be supported by a team of PM professionals, providing comprehensive programme "
                "management to coordinate multiple related projects and achieve strategic objectives."
            ),
        }
    return {"complexity": "Invalid Score", "recommendation": "Score out of expected range."}
