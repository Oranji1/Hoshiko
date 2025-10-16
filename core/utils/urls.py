from urllib.parse import parse_qs, urlparse


def clean_anidb_url(original_url: str) -> str:
    try:
        parsed_url = urlparse(original_url)
        query_params = parse_qs(parsed_url.query)

        if "aid" in query_params:
            anidb_id = query_params["aid"][0]
            return f"https://anidb.net/anime/{anidb_id}"
    except (ValueError, IndexError):
        pass

    return original_url
