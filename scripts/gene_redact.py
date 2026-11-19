# Delete Gene names from HTML

from pathlib import Path
from bs4 import BeautifulSoup


for html_file in Path(".").rglob("*.html"):
    try:
        with open(html_file, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        modified = False

        for table in soup.find_all("table"):

            # Find header row
            header_row = table.find("thead")
            if not header_row:
                continue

            headers = [
                th.get_text(strip=True)
                for th in header_row.find_all("th")
            ]

            if "Gene ID" not in headers:
                continue

            gene_col_idx = headers.index("Gene ID")

            tbody = table.find("tbody")
            if not tbody:
                continue

            for row in tbody.find_all("tr"):
                cells = row.find_all(["td", "th"])
                if len(cells) > gene_col_idx:
                    cells[gene_col_idx].string = "XXXXX"
                    modified = True

        if modified:
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(str(soup))

            print(f"Modified: {html_file}")

    except Exception as e:
        print(f"Error processing {html_file}: {e}")