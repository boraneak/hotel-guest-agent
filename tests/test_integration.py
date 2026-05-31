import os
import pytest
from dotenv import load_dotenv
from agent.rag import build_qa_chain
from agent.router import route_property

load_dotenv()

# Skip all integration tests if no API key
pytestmark = pytest.mark.skipif(
    not os.getenv("GROQ_API_KEY"),
    reason="GROQ_API_KEY not set — skipping integration tests",
)


def test_router_golden_spoon():
    assert route_property("what time does golden spoon close?") == "golden_spoon"


def test_router_azure_beach():
    assert route_property("does azure beach have a pool?") == "azure_beach"


def test_router_default():
    assert route_property("what is the wifi password?") == "grandview_hotel"


def test_rag_returns_answer():
    question = "what time does golden spoon close?"
    property_key = route_property(question)
    answer_fn = build_qa_chain(property_key)
    result = answer_fn(question)
    assert result is not None
    assert len(result) > 0
    assert "10:30" in result or "PM" in result
