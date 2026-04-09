import logging

from openai import OpenAI

from app.config import get_settings

logger = logging.getLogger(__name__)


def verify_gym_photo(image_url: str) -> bool:
    settings = get_settings()
    client = OpenAI(api_key=settings.openai_api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": image_url}},
                        {
                            "type": "text",
                            "text": (
                                "Does this image show a person at a gym or actively "
                                "exercising? Reply with only 'yes' or 'no'."
                            ),
                        },
                    ],
                }
            ],
            max_tokens=5,
        )
        answer = response.choices[0].message.content.strip().lower()
        return answer.startswith("yes")
    except Exception as e:
        logger.error("AI verification failed: %s", e)
        return False
