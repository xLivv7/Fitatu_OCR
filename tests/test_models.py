import pytest
from pydantic import ValidationError

from fitatu_ocr.schemas.nutrition import NutritionValues, ValidationWarning
from fitatu_ocr.schemas.ocr_token import OCRToken


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

def make_ocr_token(**overrides):
    '''Function for shortening tests'''
    data = {
        "text": "Obiad  ",
        "normalized_text": "obiad",
        "bbox": [10, 20, 100, 40],
        "relative_bbox": [0.1, 0.2, 0.5, 0.4],
        "confidence": 0.95,
        "source_image": "screen_01.png",
    }
    data.update(overrides)
    return OCRToken(**data)


def test_ocr_token_accepts_valid_data():
    token=make_ocr_token()
    assert token.text=="Obiad  "
    assert token.normalized_text=="obiad"
    assert token.bbox==[10, 20, 100, 40]
    assert token.relative_bbox==[0.1, 0.2, 0.5, 0.4]
    assert token.confidence==0.95
    assert token.source_image=="screen_01.png"

def test_ocr_token_rejects_relative_bbox_outside_range():
    with pytest.raises(ValidationError):
        make_ocr_token(relative_bbox=[0.1, 0.2, 1.2, 0.4])
