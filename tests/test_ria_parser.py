from app.parsers.ria_parser import RiaParser


def test_parse_article_extracts_main_fields() -> None:
    html = """
    <html>
      <body>
        <h1>Test title</h1>
        <time datetime="2026-06-01T10:30:00Z"></time>
        <div itemprop="author">Ivan Ivanov</div>
        <div class="article__text">Paragraph one.</div>
        <div class="article__text">Paragraph two.</div>
        <img src="https://cdn.example.com/1.jpg" />
        <img data-src="https://cdn.example.com/2.jpg" />
      </body>
    </html>
    """
    parser = RiaParser()

    parsed = parser.parse_article(html)

    assert parsed["title"] == "Test title"
    assert parsed["author"] == "Ivan Ivanov"
    assert parsed["full_text"] == "Paragraph one.\nParagraph two."
    assert parsed["published_at"] is not None
    assert parsed["published_at"].year == 2026
    assert parsed["image_urls"] == [
        "https://cdn.example.com/1.jpg",
        "https://cdn.example.com/2.jpg",
    ]


def test_parse_article_returns_none_when_fields_missing() -> None:
    html = "<html><body><p>no article data</p></body></html>"
    parser = RiaParser()

    parsed = parser.parse_article(html)

    assert parsed["title"] is None
    assert parsed["author"] is None
    assert parsed["full_text"] is None
    assert parsed["published_at"] is None
    assert parsed["image_urls"] == []
