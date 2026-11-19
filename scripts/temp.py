import pandas as pd
from pathlib import Path

GENE_PLOT_DIR = Path("gene plots")

# Load mapping
mapping = pd.read_csv("gene_mapping.csv")

renamed = 0

for _, row in mapping.iterrows():

    gene = str(row["original_gene"]).strip()
    anon = str(row["redacted_name"]).strip()

    old_file = GENE_PLOT_DIR / f"{gene}.png"
    new_file = GENE_PLOT_DIR / f"{anon}.png"

    if old_file.exists():
        old_file.rename(new_file)
        print(f"{old_file.name} -> {new_file.name}")
        renamed += 1
    else:
        print(f"Missing: {old_file.name}")

print(f"\nRenamed {renamed} files")