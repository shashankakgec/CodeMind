"""
Hugging Face-backed classifier integration.

Service status reports configuration only. Benchmark metrics must come from a
reproducible evaluation run and are not hardcoded here.
"""
import os
import logging
import httpx
from typing import Dict, Optional

logger = logging.getLogger(__name__)
HF_TOKEN = os.getenv("HF_TOKEN")
HF_MODEL_REPO = os.getenv("HF_MODEL_REPO", "Monkey3770/Codebert-bug-classifier")
HF_MODEL_URL = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL_REPO}"
LABEL_NAMES = ["clean", "sql_injection", "division_by_zero", "null_reference", "xss"]
CONFIDENCE_THRESHOLD = 0.65


def is_available() -> bool:
    """Return whether remote inference credentials are configured, not a health probe."""
    return bool(HF_TOKEN)


def get_metrics() -> Optional[Dict]:
    """No verified evaluation metrics are bundled with the running service."""
    return None


def predict(code: str) -> Dict:
    """Run remote inference. A configured token does not guarantee endpoint reachability."""
    if not is_available():
        return {
            "available": False,
            "message": "Hugging Face API token (HF_TOKEN) is not configured.",
            "predicted_class": None,
            "confidence": 0.0,
            "is_bug": False,
        }

    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {"inputs": code, "options": {"wait_for_model": True}}
    try:
        with httpx.Client() as client:
            response = client.post(HF_MODEL_URL, json=payload, headers=headers, timeout=20.0)

        if response.status_code != 200:
            logger.error("Hugging Face API returned status %s: %s", response.status_code, response.text[:500])
            return {
                "available": True,
                "predicted_class": "error",
                "confidence": 0.0,
                "is_bug": False,
                "error": f"Hugging Face API returned status {response.status_code}",
            }

        result = response.json()
        if isinstance(result, list) and result and isinstance(result[0], list):
            predictions = result[0]
            if not predictions or not all(
                isinstance(item, dict) and "label" in item and "score" in item
                for item in predictions
            ):
                raise ValueError("Unexpected Hugging Face prediction items")

            scores = {item["label"]: round(float(item["score"]), 4) for item in predictions}
            best = max(predictions, key=lambda item: float(item["score"]))
            pred_class = best["label"]
            confidence = float(best["score"])

            # Do not silently map unknown model labels to class zero.
            if pred_class not in LABEL_NAMES:
                return {
                    "available": True,
                    "predicted_class": "unmapped_label",
                    "model_label": pred_class,
                    "predicted_label": None,
                    "confidence": round(confidence, 4),
                    "all_scores": scores,
                    "is_bug": False,
                    "error": "Model label is not present in the application's declared label map.",
                }

            pred_idx = LABEL_NAMES.index(pred_class)
            is_bug = pred_class != "clean" and confidence >= CONFIDENCE_THRESHOLD
            return {
                "available": True,
                "predicted_class": pred_class,
                "predicted_label": pred_idx,
                "confidence": round(confidence, 4),
                "all_scores": scores,
                "is_bug": is_bug,
                "bug_type": pred_class if is_bug else None,
            }

        logger.error("Unexpected Hugging Face response format")
        return {
            "available": True,
            "predicted_class": "error",
            "confidence": 0.0,
            "is_bug": False,
            "error": "Unexpected Hugging Face response format",
        }
    except Exception as exc:
        logger.exception("Hugging Face inference failed")
        return {
            "available": True,
            "predicted_class": "error",
            "confidence": 0.0,
            "is_bug": False,
            "error": str(exc),
        }


def predict_batch(snippets: list[str]) -> list[Dict]:
    """Run prediction for multiple code snippets."""
    return [predict(snippet) for snippet in snippets]


def get_status() -> Dict:
    """Return configuration status without fabricating benchmark results."""
    configured = is_available()
    return {
        "available": configured,
        "configured": configured,
        "model_repo": HF_MODEL_REPO,
        "accuracy": None,
        "f1_macro": None,
        "metrics_available": False,
        "label_names": LABEL_NAMES,
        "threshold": CONFIDENCE_THRESHOLD,
        "message": (
            "Hugging Face credentials configured; remote endpoint reachability and benchmark metrics "
            "have not been verified by this status check."
            if configured else "Model not configured. HF_TOKEN is not set."
        ),
    }
