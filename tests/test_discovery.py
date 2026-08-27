from services.discovery import build_discovery_queries


def test_build_discovery_queries_includes_buy_and_site():
    qs = build_discovery_queries("چای")
    assert any("خرید" in q for q in qs)
    assert any("site:.ir" in q for q in qs)
    assert all("چای" in q for q in qs)
