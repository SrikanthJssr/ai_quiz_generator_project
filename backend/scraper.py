# backend/scraper.py
import requests
from bs4 import BeautifulSoup
import re
from typing import Tuple, Optional, List, Dict

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def extract_text_from_wiki(url: str) -> Tuple[Optional[str], Optional[str], Optional[Dict]]:
    """
    Scrapes the Wikipedia article (HTML) and returns:
      - title (str)
      - cleaned_text (str) : main article paragraphs concatenated
      - extras (dict) containing summary, sections list, maybe empty lists for key_entities
    Returns (None, None, None) on failure.
    """
    try:
        if "wikipedia.org/wiki/" not in url:
            return None, None, None

        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            return None, None, None

        soup = BeautifulSoup(r.text, "html.parser")

        # Title
        title_tag = soup.find("h1", id="firstHeading")
        title = title_tag.get_text(strip=True) if title_tag else ""

        # Main content
        content = soup.find("div", id="mw-content-text")
        if not content:
            # fallback: paragraphs
            paras = soup.find_all("p")
            text = " ".join(p.get_text(" ", strip=True) for p in paras)
        else:
            # remove references, tables, boxes, navboxes etc
            for s in content.select("sup, table, style, script, .mw-editsection, .reference, .infobox, .navbox"):
                s.decompose()

            paragraphs = content.find_all("p")
            text = " ".join(p.get_text(" ", strip=True) for p in paragraphs)

        # Clean bracket citations like [1]
        text = re.sub(r"\[\d+\]", "", text)
        text = re.sub(r"\s+", " ", text).strip()

        # Short summary (first 2-3 paragraphs)
        summary = ""
        try:
            first_paras = content.find_all("p")[:3] if content else []
            summary = " ".join(p.get_text(" ", strip=True) for p in first_paras)
            summary = re.sub(r"\[\d+\]", "", summary)
            summary = summary.strip()
        except Exception:
            summary = (text[:800] + "...") if text else ""

        # Sections (h2 texts)
        sections = [h.get_text(" ", strip=True) for h in content.find_all(["h2", "h3"])] if content else []

        extras = {
            "summary": summary,
            "sections": sections,
            "key_entities": {"people": [], "organizations": [], "locations": []}
        }

        return title, text, extras

    except Exception as e:
        # print or log if needed
        return None, None, None
