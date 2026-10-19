# Mosaic Generator

This desktop Python application turns a target image into a photo mosaic. Each
target cell is replaced with the source image whose average color is closest
to that cell.

Input:
<img width="967" height="651" alt="image" src="https://github.com/user-attachments/assets/f6b19180-28cd-433a-80a7-7e56800e9655" />

Output:
<img width="981" height="661" alt="image" src="https://github.com/user-attachments/assets/f568a858-d1e6-4a53-aefc-0c489e4986cc" />

Input: 
<img width="970" height="656" alt="Screenshot 2026-10-18 225121" src="https://github.com/user-attachments/assets/6244d8a2-b707-40b3-bea0-f01decd52d1c" />

Output: 
<img width="972" height="661" alt="image" src="https://github.com/user-attachments/assets/922bafdc-9c0f-489a-b5e5-cb1b21dd0120" />



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
