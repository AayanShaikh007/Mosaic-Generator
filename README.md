# Mosaic Generator

This desktop Python application turns a target image into a photo mosaic. Each
target cell is replaced with the source image whose average color is closest
to that cell.

<img width="981" height="661" alt="image" src="https://github.com/user-attachments/assets/f568a858-d1e6-4a53-aefc-0c489e4986cc" />


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
