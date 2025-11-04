def validate_text_input(text: str) -> str:
    if not text or not text.strip():
        raise ValueError("Text input cannot be empty")
    return text.strip()


def validate_positive_float(value: float, name: str) -> float:
    if value < 0 or value > 1:
        raise ValueError(f"{name} must be between 0 and 1")
    return value
