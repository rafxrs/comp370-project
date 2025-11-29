from src.utils.news_api_fetcher import ArticleFetcher

def test_api_fetch(tmp_output):
    fetcher = ArticleFetcher(
        search_term="Netanyahu",
        sources=["globalnews.ca", "cbc.ca"],
        target_count=3,
        start_date="2024-01-01"
    )

    articles = fetcher.fetch_articles()

    # Should fetch SOME articles from these sources
    assert len(articles) > 0
    assert len(articles) <= 3

    for a in articles:
        assert "source" in a
        assert a["source"] in ["globalnews.ca", "cbc.ca"]
        assert "date" in a
        assert "title" in a
        assert "opening" in a
        assert "open_coding" not in a
        assert "coding" not in a
        assert "sentiment" not in a

