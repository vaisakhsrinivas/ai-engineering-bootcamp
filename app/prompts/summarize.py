"""
Four prompt strategies for summarization:
- zero_shot: single instruction with text and max_length
- few_shot: instruction + 1-2 examples, then target text
- chain_of_thought: list main points then write summary in at most N words
- meta: act as expert summarizer, consider audience and length
"""

from typing import Literal

PromptType = Literal["zero_shot", "few_shot", "chain_of_thought", "meta"]


def build_messages(prompt_type: PromptType, text: str, max_length: int) -> list[dict[str, str]]:
    """Return messages list for OpenAI Chat Completions."""
    if prompt_type == "zero_shot":
        return _zero_shot(text, max_length)
    if prompt_type == "few_shot":
        return _few_shot(text, max_length)
    if prompt_type == "chain_of_thought":
        return _chain_of_thought(text, max_length)
    if prompt_type == "meta":
        return _meta(text, max_length)
    raise ValueError(f"Unknown prompt_type: {prompt_type}")


def _zero_shot(text: str, max_length: int) -> list[dict[str, str]]:
    return [
        {
            "role": "user",
            "content": f"Summarize the following text in at most {max_length} words. Be concise and preserve the main ideas.\n\nText:\n{text}",
        }
    ]


def _few_shot(text: str, max_length: int) -> list[dict[str, str]]:
    return [
        {
            "role": "user",
            "content": """Summarize the following text in at most {0} words. Be concise and preserve the main ideas.

Example 1:
Input: "The company reported record profits this quarter. Revenue increased by 20% year over year. The CEO announced expansion into three new markets."
Summary (max 15 words): Company had record profits; revenue up 20%. CEO announced expansion into three new markets.

Example 2:
Input: "Climate change is affecting global weather patterns. Scientists urge immediate action to reduce carbon emissions. Governments are meeting next month to discuss new targets."
Summary (max 15 words): Climate change alters weather; scientists urge emission cuts. Governments to meet on new targets.

Now summarize the following text in at most {0} words:

Text:
{1}""".format(
                max_length, text
            ),
        }
    ]


def _chain_of_thought(text: str, max_length: int) -> list[dict[str, str]]:
    return [
        {
            "role": "user",
            "content": f"""First, list the main points or key ideas in the following text. Then, write a concise summary in at most {max_length} words that captures those points.

Text:
{text}

Provide your answer in this format:
Main points:
1. ...
2. ...

Summary (at most {max_length} words):""",
        }
    ]


def _meta(text: str, max_length: int) -> list[dict[str, str]]:
    return [
        {
            "role": "user",
            "content": f"""You are an expert summarizer. Your task is to produce a clear, accurate summary suited for a general audience.

Consider:
- The main message and supporting details
- The length constraint: at most {max_length} words
- Clarity and readability

Summarize the following text in at most {max_length} words:

Text:
{text}""",
        }
    ]
