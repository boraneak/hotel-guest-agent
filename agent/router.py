PROPERTY_KEYWORDS = {
    "grandview_hotel": [
        "grandview",
        "grandview hotel",
        "hotel",
        "resort hotel",
    ],
    "golden_spoon": [
        "golden spoon",
        "restaurant",
        "dim sum",
        "food",
        "dining",
    ],
    "azure_beach": [
        "azure",
        "azure beach",
        "beach resort",
        "beach",
        "resort",
    ],
}

DEFAULT_PROPERTY = "grandview_hotel"


def route_property(message: str) -> str:
    message_lower = message.lower()

    for property_key, keywords in PROPERTY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in message_lower:
                return property_key

    return DEFAULT_PROPERTY
