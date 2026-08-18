from filters import passes_filter


def test_technique_item_passes():
    assert passes_filter(
        "Startup Debuts Biofabricated Leather Alternative",
        "A new material grown from mycelium mimics leather's texture.",
    ) is True


def test_celebrity_item_is_excluded_even_with_a_keyword():
    assert passes_filter(
        "Kardashian Wore a Recycled Denim Look on the Red Carpet",
        "The reality star wore a custom denim gown.",
    ) is False


def test_unrelated_business_item_is_excluded():
    assert passes_filter(
        "Retailer Reports Quarterly Earnings Above Expectations",
        "Shares rose after the company posted strong revenue.",
    ) is False


def test_item_without_any_technique_keyword_is_excluded():
    assert passes_filter(
        "Designer Opens New Flagship Store in Milan",
        "The store features an updated interior layout.",
    ) is False


def test_retail_store_opening_is_excluded_even_with_a_keyword():
    assert passes_filter(
        "Still Here Denim Brand Opens West Village Boutique",
        "The denim label's new retail space anchors its direct-to-consumer growth.",
    ) is False


def test_retail_shop_experience_is_excluded_even_with_a_keyword():
    assert passes_filter(
        "Revolve Opens Cotton Shop Experience in Chicago",
        "The customization concept lets shoppers personalize denim in store.",
    ) is False
