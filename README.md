# Labeling app

This repo was created to facilitate the labeling of the images. It was built with 'PyQt' and has a field for entering the folder with the images, a field for entering the folder with all labels, and two buttons clickable with 'i' and 'j' keyboard key, which will mark the image shown in the field as 1 for a glass and 0 for empty space (obviously in the txt file, e.g. 'gt_2024-09-04_14-26-59_1.txt'). The window will show you also all allready labeled images. By clicking one of the buttons, it will load the next image from the list to label it.

## Setup

create a `python3.10` virtual environment by typing the following command in the terminal:

```bash
python3.10 -m venv .venv
```

Then install all dependencies by:

```bash
pip install -r requirements.txt
```

Afterwards run:

```bash
python main.py
```
