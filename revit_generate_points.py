# Import required .NET interop tools
import clr
import os

# Add references to Revit API assemblies so we can use their classes in Python
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
clr.AddReference('RevitAPIUI')

# Import classes from the Revit API
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI.Selection import ObjectType

# Import access to the current Revit document from pyRevit/RevitServices
from RevitServices.Persistence import DocumentManager

# Get the current active Revit document
doc = DocumentManager.Instance.CurrentDBDocument

# Get access to the UI document (needed for user selections)
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

# Function to order a list of curve segments so they form a continuous path
def chain_curves(curves, tol=1e-6):
    if not curves:
        return []
    chain = [curves.pop(0)]  # Start with the first curve
    while curves:
        last = chain[-1]
        end = last.GetEndPoint(1)  # Get the end point of the last curve in the chain
        found = False
        for i, c in enumerate(curves):
            # Check if the start of this curve matches the end of the last one
            if c.GetEndPoint(0).IsAlmostEqualTo(end, tol):
                chain.append(curves.pop(i))
                found = True
                break
            # If the *end* of this curve matches the last end point, reverse it
            elif c.GetEndPoint(1).IsAlmostEqualTo(end, tol):
                chain.append(curves.pop(i).CreateReversed())
                found = True
                break
        if not found:
            # Break if we can't find a connecting curve (possibly open curve)
            break
    return chain

# Function to sample evenly spaced points along a curve
def sample_curve(curve, num_points):
    # Evaluate points at normalized parameters between 0 and 1
    return [curve.Evaluate(i / float(num_points), True) for i in range(num_points + 1)]

# Ask the user to select a curve-based element from the model
ref = uidoc.Selection.PickObject(ObjectType.Element, "Select a curve-based element")
element = doc.GetElement(ref)

# Get the geometry of the selected element with default options
geometry = element.get_Geometry(Options())

# Extract only curve objects (Line, Arc, NurbSpline, etc.) from the geometry
raw_curves = [g for g in geometry if isinstance(g, Curve)]

# Order the curves into a continuous path (if possible)
ordered_curves = chain_curves(raw_curves)

# Number of points to sample per curve segment
points_per_curve = 50

# List to store all sampled XYZ points
all_points = []

# Loop through each ordered curve and sample points
for i, curve in enumerate(ordered_curves):
    sampled = sample_curve(curve, points_per_curve)
    if i > 0:
        # Skip the first point to avoid duplicates at curve joints
        sampled = sampled[1:]
    all_points.extend(sampled)

# Define output file path in user's Documents folder
filename = "sampled_curve_points.txt"
output_path = os.path.join(os.path.expanduser("~"), "Documents", filename)

# Write all sampled points to the output text file
with open(output_path, "w") as f:
    for pt in all_points:
        # Format each point as X,Y,Z with 6 decimal places
        f.write(f"{pt.X:.6f},{pt.Y:.6f},{pt.Z:.6f}\n")

# Print result to the Revit Python output console
print(f"{len(all_points)} points written to: {output_path}")