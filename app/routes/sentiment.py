import json
import re
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.llm import complete
from app.prompts import sentiment as sentiment_prompts

router = APIRouter()
PromptType = Literal["zero_shot", "few_shot", "chain_of_thought", "meta"]

SentimentLabel = Literal["positive", "negative", "neutral"]


class AnalyzeSentimentRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to analyze")
    prompt_type: PromptType = Field(
        default="zero_shot",
        description="Prompt strategy: zero_shot, few_shot, chain_of_thought, meta",
    )


class AnalyzeSentimentResponse(BaseModel):
    sentiment: SentimentLabel
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    explanation: str


def _parse_sentiment_response(raw: str) -> dict:
    """Parse LLM response to extract sentiment, confidence_score, explanation. Handles JSON in code blocks."""
    raw = raw.strip()
    # Strip markdown code block if present
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("Expected JSON object")
    sentiment = (data.get("sentiment") or "").strip().lower()
    if sentiment not in ("positive", "negative", "neutral"):
        raise ValueError(f"Invalid sentiment: {sentiment}")
    confidence = data.get("confidence_score")
    if confidence is None:
        raise ValueError("Missing confidence_score")
    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        raise ValueError("confidence_score must be a number")
    if not (0 <= confidence <= 1):
        raise ValueError("confidence_score must be between 0 and 1")
    explanation = data.get("explanation") or data.get("reasoning") or ""
    if isinstance(explanation, str):
        explanation = explanation.strip()
    else:
        explanation = str(explanation)
    return {
        "sentiment": sentiment,
        "confidence_score": confidence,
        "explanation": explanation or "No explanation provided.",
    }


@router.post("", response_model=AnalyzeSentimentResponse)
def analyze_sentiment(request: AnalyzeSentimentRequest):
    """Analyze sentiment of text. Returns sentiment, confidence_score (0-1), and explanation."""
    try:
        messages = sentiment_prompts.build_messages(request.prompt_type, request.text)
        result = complete(messages, max_tokens=400)
        parsed = _parse_sentiment_response(result)
        return AnalyzeSentimentResponse(**parsed)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail="LLM service unavailable")
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=502, detail="Invalid response from LLM")
    except Exception as e:
        raise HTTPException(status_code=502, detail="LLM request failed")
