from agent.router import route_property


def test_golden_spoon_by_name():
    assert route_property("what time does golden spoon close?") == "golden_spoon"


def test_azure_beach_by_name():
    assert route_property("does azure beach have a pool?") == "azure_beach"


def test_grandview_by_name():
    assert route_property("grandview hotel check in time") == "grandview_hotel"


def test_default_when_no_keyword():
    assert route_property("what is the wifi password?") == "grandview_hotel"


def test_case_insensitive():
    assert route_property("GOLDEN SPOON menu") == "golden_spoon"


def test_empty_message():
    assert route_property("") == "grandview_hotel"


def test_food_keyword():
    assert route_property("where can I get food?") == "golden_spoon"


def test_beach_keyword():
    assert route_property("I want to go to the beach") == "azure_beach"
