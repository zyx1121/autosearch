KEYWORD = "legal thc flower shipping"
BLACKLIST_FILE = "black.txt"
SEARCH_NUM = 100

import argparse
import sys
from urllib.parse import urlparse

from googlesearch import search


def extract_base_url(url):
    """Extract base URL from a full URL."""
    parsed = urlparse(url)
    return parsed.netloc


def load_blacklist(filepath):
    """Load blacklist base URLs from file."""
    blacklist = set()
    try:
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    blacklist.add(line)
    except FileNotFoundError:
        print(
            f"Warning: Blacklist file '{filepath}' not found. Continuing without blacklist."
        )
    except Exception as e:
        print(f"Failed to read blacklist file: {e}")
        sys.exit(1)
    return blacklist


def search_with_fallback(keyword, search_num):
    """Try different parameter names for googlesearch.search for compatibility."""
    try:
        return search(keyword, num_results=search_num)
    except TypeError:
        try:
            return search(keyword, num=search_num)
        except TypeError:
            return search(keyword, stop=search_num)
        except Exception as e:
            print(f"Unknown error: {e}")
            raise
    except Exception as e:
        print(f"Unknown error: {e}")
        raise


blacklist = set()
if BLACKLIST_FILE:
    blacklist = load_blacklist(BLACKLIST_FILE)

for result in search_with_fallback(KEYWORD, SEARCH_NUM):
    base = extract_base_url(result)
    if base in blacklist:
        continue
    print(result)
