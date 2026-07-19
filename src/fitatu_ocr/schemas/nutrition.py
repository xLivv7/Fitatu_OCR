from typing import Literal
from pydantic import BaseModel, Field


class ValidationWarning(BaseModel):
    """Warning collected during parsing or validation without stopping the pipeline."""

    code: str
    message: str
    severity: Literal["info", "warning", "error"] = "warning"
    source_image: str | None = None
    field: str | None = None


class NutritionValues(BaseModel):
    """Nutrition values shared by daily summaries, meals and food items."""

    energy_kcal: float | None = Field(default=None, ge=0)
    protein_g: float | None = Field(default=None, ge=0)
    fat_g: float | None = Field(default=None, ge=0)
    carbohydrates_g: float | None = Field(default=None, ge=0)