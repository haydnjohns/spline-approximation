import clr
import os
clr.AddReference('RevitServices')
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')

from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager

# Revit document
doc = DocumentManager.Instance.CurrentDBDocument

# Parameters
n = 100  # Number of points per spline
output_path = r"C:\Users\YourUsername\Documents\spline_points.txt"

# Collect all spline curve elements
collector = FilteredElementCollector(doc).OfClass(CurveElement)
splines = [e for e in collector if isinstance(e.GeometryCurve, NurbSpline)]

# Open file for writing
with open(output_path, "w") as f:
    for spline in splines:
        nurbs = spline.GeometryCurve
        param_start = nurbs.GetEndParameter(0)
        param_end = nurbs.GetEndParameter(1)

        for i in range(n):
            t = param_start + (param_end - param_start) * (float(i) / (n - 1))
            pt = nurbs.Evaluate(t, False)
            line = f"{pt.X},{pt.Y},{pt.Z}\n"
            f.write(line)

print(f"Points written to: {output_path}")