from pydantic import BaseModel, Field, model_validator


class OCRToken(BaseModel):
    """Single OCR text fragment with absolute and relative coordinates."""    
    
    text: str
    normalized_text: str
    bbox: list[float] = Field(min_length=4, max_length=4)
    relative_bbox: list[float] = Field(min_length=4, max_length=4)
    confidence: float | None = Field(default=None, ge=0, le=1)
    source_image: str

    @model_validator(mode="after")
    def validate_bbox_order(self) -> "OCRToken":
        x1, y1, x2, y2 = self.bbox
        if x2 < x1 or y2 < y1:
            raise ValueError("bbox must be ordered as [x1, y1, x2, y2]")

        rx1, ry1, rx2, ry2 = self.relative_bbox
        if rx2 < rx1 or ry2 < ry1:
            raise ValueError("relative_bbox must be ordered as [x1, y1, x2, y2]")

        if any(value < 0 or value > 1 for value in self.relative_bbox):
            raise ValueError("relative_bbox values must be between 0 and 1")

        return self