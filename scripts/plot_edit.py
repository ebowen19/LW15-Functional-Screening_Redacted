from pathlib import Path
import matplotlib.pyplot as plt

# 30 pixels @ top for Graeber, 100 for TCGA & Gene Plots

input_folder = Path(r"TCGA/survival_curves/non-significant")

for file in input_folder.rglob("*"):
    if file.suffix.lower() == ".png":
        print(file)
        img = plt.imread(file)

        cropped = img[100:, :]

        plt.imsave(input_folder / file.name, cropped)