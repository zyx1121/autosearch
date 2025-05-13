import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
import typer
from googlesearch import search
from rich import print

app = typer.Typer()


def load_blacklist(filepath: Path) -> set[str]:
    """
    Load blacklist base URLs from file.
    """
    blacklist = set()
    try:
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    blacklist.add(line)
    except FileNotFoundError:
        print(f"[WARN] Blacklist '{filepath}' not found. Creating empty blacklist.")
        Path(filepath).touch()
    except Exception as e:
        print(f"[ERROR] Failed to read blacklist file: {e}")
        sys.exit(1)
    return blacklist


@app.command()
def autosearch(
    keyword: str,
    num_search: int = 50,
    blacklist_file: Path = Path("blacklist.txt"),
    output: Path = Path("results.csv"),
):
    """
    Search for a keyword and save results to CSV.
    """
    blacklist = load_blacklist(blacklist_file)
    results = []
    for result in search(keyword, num_results=num_search):
        if urlparse(result).netloc in blacklist:
            continue
        print(f"[INFO] {result}")
        results.append(result)
        time.sleep(0.01)
    df = pd.DataFrame(results, columns=["url"])
    df.to_csv(output, index=False)
    print(f"[INFO] Results saved to [bold green]{output}[/bold green]")


if __name__ == "__main__":
    app()
