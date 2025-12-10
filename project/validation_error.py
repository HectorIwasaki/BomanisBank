class ValidationError(ValueError):
    pass

def require_field(value: str | None, name: str) -> str:
    """Ensures that a required field is provided."""
    if value is None or (isinstance(value, str) and value.strip() == ""):
        raise ValidationError(f"{name} is required")
    return value