# Standard imports
from typing import List, Set, Tuple
import logging
import re
import urllib.parse

# Library imports
import requests

def yoink(version: str, book: str, chapter: str, verse: int = -1, verseRange: Tuple[int, int] = None) -> str:
    html = download_reference_html(f"{book} {chapter}", version)
    # TODO: add filter method here based on what the value of verses is. 
    # TODO: regardless, remove all verse numbers here. 
    return extract_reference_text(html)


def download_reference_html(verse_ref: str, version: str) -> str:
    """Pulls HTML from BibleGateway"""

    # Encode the verse ref so we can pass it to gateway
    verse_ref_encoded = urllib.parse.quote(verse_ref)

    # Construct url
    url = f"https://www.biblegateway.com/passage/?search={verse_ref_encoded}&version={version}"

    # Pull page from gateway
    response = requests.get(url, timeout=10)

    # Done.
    logging.debug(response.text)
    return response.text


# TODO: add filter method here. 

# TODO: remove all verse 


def extract_reference_text(html: str) -> str:
    """Given HTML from BG, pull out just the Scripture text and keeps verse numbers."""

    # Use a regex pattern to find the correct content div
    match = re.search(
        r'<div class=\'passage-content passage-class-0.*?>(.*?)</div>',
        html,
        re.DOTALL
    )

    if not match:
        print(html)
        raise SyntaxError("Couldn't find verse content")

    # Get the verse text from the match
    verse_text = match.group(1).strip()

    # Remove all other <sup> tags and keep only the number inside
    verse_text = re.sub(r'<sup[^>]*>(.*?)</sup>', r'\1', verse_text, flags=re.IGNORECASE)

    # Scrub metadata
    verse_text = re.sub(r'<div [^>]+>', '', verse_text)
    verse_text = re.sub(r'<h3>.*?</h3>', '', verse_text)
    verse_text = re.sub(r'<p[^>]*>', '', verse_text)
    verse_text = re.sub(r'</p>', ' ', verse_text)
    verse_text = re.sub(r'<span[^>]*>', ' ', verse_text)
    verse_text = re.sub(r'</span>', ' ', verse_text)
    verse_text = re.sub(r'<a[^>]*>', '', verse_text)
    verse_text = re.sub(r'</a>', '', verse_text)
    verse_text = re.sub(r'<br[^>]*>', ' ', verse_text)
    verse_text = re.sub(r'&nbsp;', ' ', verse_text)
    verse_text = re.sub(r'\s+', ' ', verse_text)  # Replace multiple spaces with a single space
    verse_text = verse_text.strip()

    # All done.
    return verse_text


# print(extract_reference_text(download_reference_html()))
print(yoink("Genesis 2", "KJV"))