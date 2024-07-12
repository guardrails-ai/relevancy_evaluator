# to run these, run 
# make tests

from guardrails import Guard
import pytest
from validator import RelevancyEvaluator

# We use 'exception' as the validator's fail action,
# so we expect failures to always raise an Exception
# Learn more about corrective actions here:
# https://www.guardrailsai.com/docs/concepts/output/#%EF%B8%8F-specifying-corrective-actions
guard = Guard.from_string(validators=[RelevancyEvaluator(llm_callable="gpt-3.5-turbo", on_fail="exception")])

def test_pass():
    test_value = {
        "original_prompt": "What is the capital of France?",
        "reference_text": "The capital of France is Paris."
    }
    result = guard.parse(test_value)
  
    assert result.validation_passed is True
    assert result.validated_output == test_value

def test_fail():
    with pytest.raises(Exception) as exc_info:
        test_value = {
            "original_prompt": "What is the capital of France?",
            "reference_text": "France is a country in Europe."
        }
        guard.parse(test_value)
  
    assert str(exc_info.value) == "The LLM says 'unrelated'. The validation failed."
