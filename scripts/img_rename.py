# take gene names out of img names in html & in repo
# case-insensitive

from pathlib import Path
import re

# =====================================================
# CONFIG
# =====================================================

ROOT = Path(".")
GENE_PLOT_DIR = ROOT / "gene plots"

# =====================================================
# BUILD GENE -> GENE_### MAPPING
# =====================================================

gene_names = sorted(
    p.stem
    for p in GENE_PLOT_DIR.glob("*.png")
)

gene_map = {
    gene: f"GENE_{i:03d}"
    for i, gene in enumerate(gene_names, start=1)
}

print(f"Found {len(gene_map)} genes")

# Save mapping
with open("gene_mapping.csv", "w", encoding="utf-8") as f:
    f.write("original_gene,redacted_name\n")

    for gene, anon in gene_map.items():
        f.write(f"{gene},{anon}\n")

print("Saved gene_mapping.csv")

# =====================================================
# SORT LONGEST FIRST
# prevents partial replacement issues
# =====================================================

sorted_genes = sorted(
    gene_map.items(),
    key=lambda x: len(x[0]),
    reverse=True,
)

# =====================================================
# RENAME PNG FILES
# =====================================================

all_pngs = list(ROOT.rglob("*.png"))

rename_count = 0

for png in all_pngs:

    new_name = png.name

    for gene, anon in sorted_genes:

        pattern = re.compile(
            re.escape(gene),
            flags=re.IGNORECASE
        )

        new_name = pattern.sub(
            anon,
            new_name
        )

    if new_name != png.name:

        new_path = png.with_name(new_name)

        print(f"RENAMING: {png.name}")
        print(f"       -> {new_name}")

        png.rename(new_path)

        rename_count += 1

print(f"\nRenamed {rename_count} PNG files")

# =====================================================
# UPDATE ALL HTML FILES
# =====================================================

html_count = 0

for html_file in ROOT.rglob("*.html"):

    print(f"Updating {html_file}")

    text = html_file.read_text(
        encoding="utf-8",
        errors="ignore"
    )

    original_text = text

    for gene, anon in sorted_genes:

        text = re.sub(
            re.escape(gene),
            anon,
            text,
            flags=re.IGNORECASE
        )

    if text != original_text:

        html_file.write_text(
            text,
            encoding="utf-8"
        )

        html_count += 1

print(f"\nUpdated {html_count} HTML files")

print("\nDone.")