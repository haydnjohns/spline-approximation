# Spline Approximation & Revit Point Extraction

This project contains tools for:

- Approximating 2D and 3D splines using Python.
- Extracting evenly spaced `(x, y, z)` coordinates from spline curves in Autodesk Revit using the Revit API.
- Exporting spline data to `.txt` files for further analysis or visualization.

## 📁 Project Structure

```
├── 2D_spline_approximation.py      # Approximate and analyze 2D splines
├── 3D_spline_approximation.py      # Approximate and analyze 3D splines
├── get-tree.py                     # [Ignored] Utility script (not tracked)
├── original_spline.txt             # [Ignored] Input data for 2D splines
├── original_spline_3d.txt          # [Ignored] Input data for 3D splines
└── revit_generate_points.py        # RevitPythonShell script to extract spline points
```

## 🛠 Requirements

- Python 3.x for 2D/3D spline scripts
- Autodesk Revit with:
  - **pyRevit** or **RevitPythonShell** for running `revit_generate_points.py`
  - Access to Revit API (`RevitAPI.dll`, `RevitServices.dll`, etc.)

## 🔧 Usage

### Python (2D/3D spline approximation)
```bash
python 2D_spline_approximation.py
python 3D_spline_approximation.py
```

### Revit (Extract spline points)
1. Open Revit and load the script with pyRevit or RevitPythonShell.
2. Ensure splines exist in your model.
3. Run the script to export coordinates to `.txt`.

## 📄 Output Format

Extracted points are saved in plain text format:

```
x1,y1,z1
x2,y2,z2
...
```

## 📦 License

MIT License (or specify your preferred license)

## 🙌 Contributions

Feel free to fork, submit issues, or open pull requests!
