"""Phase 2: GPT-4o vision verification service."""


async def verify_gym_photo(photo_url: str) -> dict:
    """
    Send the photo to GPT-4o vision and return a dict with:
      { "verified": bool, "confidence_score": float, "reason": str }
    """
    raise NotImplementedError("AI verification not implemented until Phase 2")
