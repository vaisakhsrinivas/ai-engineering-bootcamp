"""
Four prompt strategies for sentiment analysis:
- zero_shot: classify sentiment, provide confidence (0-1) and explanation
- few_shot: same with 2-3 examples
- chain_of_thought: first explain what suggests the sentiment, then label, confidence, explanation
- meta: act as sentiment analyst, consider tone, intensity, mixed signals
"""

from typing import Literal

PromptType = Literal["zero_shot", "few_shot", "chain_of_thought", "meta"]


def build_messages(prompt_type: PromptType, text: str) -> list[dict[str, str]]:
    """Return messages list for OpenAI Chat Completions."""
    if prompt_type == "zero_shot":
        return _zero_shot(text)
    if prompt_type == "few_shot":
        return _few_shot(text)
    if prompt_type == "chain_of_thought":
        return _chain_of_thought(text)
    if prompt_type == "meta":
        return _meta(text)
    raise ValueError(f"Unknown prompt_type: {prompt_type}")


def _zero_shot(text: str) -> list[dict[str, str]]:
    return [
        {
            "role": "user",
            "content": f"""Classify the sentiment of the following text as positive, negative, or neutral. Provide:
1. sentiment: one of positive, negative, neutral
2. confidence_score: a number between 0 and 1
3. explanation: a brief explanation

Respond in valid JSON only, with keys: "sentiment", "confidence_score", "explanation"

Text:
{text}""",
        }
    ]


def _few_shot(text: str) -> list[dict[str, str]]:
    return [
        {
            "role": "user",
            "content": f"""Classify the sentiment of the text as positive, negative, or neutral. Provide sentiment, confidence_score (0-1), and a brief explanation. Respond in valid JSON with keys: "sentiment", "confidence_score", "explanation".

Examples:

Text: "I love this product! Best purchase ever."
{{"sentiment": "positive", "confidence_score": 0.95, "explanation": "Strong positive language and enthusiasm."}}

Text: "The service was slow and the staff was rude."
{{"sentiment": "negative", "confidence_score": 0.9, "explanation": "Explicit negative descriptors."}}

Text: "The meeting is at 3 PM in room 4."
{{"sentiment": "neutral", "confidence_score": 0.85, "explanation": "Factual statement with no emotional content."}}

Now analyze the following text and respond with JSON only:

Text:
{text}""",
        }
    ]


def _chain_of_thought(text: str) -> list[dict[str, str]]:
    return [
        {
            "role": "user",
            "content": f"""First, explain what in the text suggests the sentiment (word choice, tone, context). Then give your classification.

Respond in valid JSON with:
- "reasoning": your brief step-by-step reasoning
- "sentiment": one of positive, negative, neutral
- "confidence_score": number between 0 and 1
- "explanation": short summary for the user

Text:
{text}""",
        }
    ]


def _meta(text: str) -> list[dict[str, str]]:
    return [
        {
            "role": "user",
            "content": f"""You are a sentiment analyst. Consider tone, intensity, and any mixed signals in the text. Output your analysis as valid JSON with:
- "sentiment": one of positive, negative, neutral
- "confidence_score": number between 0 and 1
- "explanation": brief explanation for the user

Text:
{text}""",
        }
    ]
