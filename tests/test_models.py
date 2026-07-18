import pytest
from pydantic import ValidationError

from fitatu_ocr.schemas.nutrition import NutritionValues, ValidationWarning


def test_validation_warning_uses_default_severity():
    warning = ValidationWarning(code="missing_value", message="Missing kcal value")

    assert warning.severity == "warning"
    assert warning.source_image is None


def test_nutrition_values_accept_valid_numbers():
    values = NutritionValues(
        energy_kcal=359,
        protein_g=7.8,
        fat_g=1.0,
        carbohydrates_g=79.0,
    )

    assert values.energy_kcal == 359
    assert values.protein_g == 7.8


def test_nutrition_values_allow_missing_values():
    values = NutritionValues()

    assert values.energy_kcal is None
    assert values.protein_g is None
    assert values.fat_g is None
    assert values.carbohydrates_g is None


def test_nutrition_values_reject_negative_numbers():
    with pytest.raises(ValidationError):
        NutritionValues(energy_kcal=-1)
