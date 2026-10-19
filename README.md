# Mosaic Generator

This desktop Python application turns a target image into a photo mosaic. Each
target cell is replaced with the source image whose average color is closest
to that cell.

## Setup

Use Python 3.10 or newer. From this directory:

```powershell
py -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

## Run

Launch the desktop application:

```powershell
.venv\Scripts\python main.py
```

The application includes four sample target images and two source collections.
You can also choose another image from disk. The generated image is written to
`finalproduct.jpg`.

The generator can also be used without the GUI:

```powershell
.venv\Scripts\python mosaic.py
```
