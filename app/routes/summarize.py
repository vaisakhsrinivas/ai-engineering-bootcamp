from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.llm import complete
from app.prompts import summarize as summarize_prompts

router = APIRouter()
PromptType = Literal["zero_shot", "few_shot", "chain_of_thought", "meta"]


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to summarize")
    max_length: int = Field(..., ge=1, le=500, description="Maximum summary length in words")
    prompt_type: PromptType = Field(
        default="zero_shot",
        description="Prompt strategy: zero_shot, few_shot, chain_of_thought, meta",
    )


class SummarizeResponse(BaseModel):
    summary: str


@router.post("", response_model=SummarizeResponse)
def summarize(request: SummarizeRequest):
    """Summarize text using the specified prompt strategy. Returns summary only."""
    try:
        messages = summarize_prompts.build_messages(
            request.prompt_type, request.text, request.max_length
        )
        result = complete(messages, max_tokens=min(512, request.max_length * 2))
        return SummarizeResponse(summary=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail="LLM service unavailable")
    except Exception as e:
        raise HTTPException(status_code=502, detail="LLM request failed")
