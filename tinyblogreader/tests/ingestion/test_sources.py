from pathlib import Path

from tinyblogreader.ingestion.sources import BlogSource, load_sources


def test_load_sources(tmp_path: Path):
    expected_source = BlogSource.model_validate(
        {
            "name": "Netflix Tech Blog",
            "url": "https://netflixtechblog.com",
            "feed_url": "http://techblog.netflix.com/feeds/posts/default",
        }
    )
    yaml_content = """
    - name: Netflix Tech Blog
      url: https://netflixtechblog.com
      feed_url: http://techblog.netflix.com/feeds/posts/default
    """

    sources_file = tmp_path / "sources.yaml"
    _ = sources_file.write_text(yaml_content)

    sources = load_sources(sources_file)
    assert len(sources) == 1
    assert sources[0] == expected_source
