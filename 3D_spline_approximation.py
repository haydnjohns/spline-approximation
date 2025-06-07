import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
from time import time

# === Generate points along a pseudo-spline ===
def generate_spline_points_3d(
    filename="original_spline_3d.txt",
    num_points=100_000,
    x_range=(0, 10),
    y_scale=1.0,
    z_scale=1.0,
    show_graph=False,
    random_seed=42
):
    np.random.seed(random_seed)
    x = np.linspace(x_range[0], x_range[1], num_points)

    # Gentle variation in Y: low-order curve + light wave
    y = (
        0.05 * x**2
        - 0.3 * x
        + 0.2 * np.sin(0.8 * x)
    )

    # Gentle Z: slow cosine wave with small bumps
    z = (
        0.3 * np.cos(0.6 * x)
        + 0.1 * np.sin(1.2 * x)
    )

    y_centered = y - np.mean(y)
    z_centered = z - np.mean(z)

    y_scaled = (y_centered / np.max(np.abs(y_centered))) * y_scale
    z_scaled = (z_centered / np.max(np.abs(z_centered))) * z_scale

    if show_graph:
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(x, y_scaled, z_scaled, linewidth=0.7)
        ax.set_title("Smooth 3D Spline Curve")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        plt.tight_layout()
        plt.show()

    with open(filename, "w") as f:
        for x_val, y_val, z_val in zip(x, y_scaled, z_scaled):
            f.write(f"{x_val},{y_val},{z_val}\n")

    print(f"Text file '{filename}' saved with {num_points} calm 3D points.")
    return [(x_val, y_val, z_val) for x_val, y_val, z_val in zip(x, y_scaled, z_scaled)]

# === Read 3D Points ===
def read_points_3d(filename):
    with open(filename, 'r') as f:
        return [tuple(map(float, line.strip().split(','))) for line in f]

# === Perpendicular Distance in 3D ===
def perpendicular_distance_3d(pt, line_start, line_end):
    px, py, pz = pt
    x1, y1, z1 = line_start
    x2, y2, z2 = line_end

    if (x1 == x2) and (y1 == y2) and (z1 == z2):
        return math.dist(pt, line_start)

    # Vector math: find projection of vector AP onto AB, then distance to line
    A = np.array([x1, y1, z1])
    B = np.array([x2, y2, z2])
    P = np.array([px, py, pz])

    AB = B - A
    AP = P - A
    t = np.dot(AP, AB) / np.dot(AB, AB)
    t = np.clip(t, 0, 1)

    closest = A + t * AB
    return np.linalg.norm(P - closest)

# === Douglas-Peucker in 3D ===
def douglas_peucker_3d(points, epsilon):
    start, end = points[0], points[-1]

    max_dist = 0
    index = 0
    for i in range(1, len(points) - 1):
        dist = perpendicular_distance_3d(points[i], start, end)
        if dist > max_dist:
            max_dist = dist
            index = i

    if max_dist > epsilon:
        left = douglas_peucker_3d(points[:index+1], epsilon)
        right = douglas_peucker_3d(points[index:], epsilon)
        return left[:-1] + right
    else:
        return [start, end]

# === Plot 3D Result ===
def plot_simplification_3d(original, simplified):
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111, projection='3d')

    x_orig, y_orig, z_orig = zip(*original)
    x_simp, y_simp, z_simp = zip(*simplified)

    ax.plot(x_orig, y_orig, z_orig, 'k-', linewidth=0.5, label='Original Curve')
    ax.scatter(x_orig, y_orig, z_orig, c='gray', s=0.1, label='Original Points')

    ax.plot(x_simp, y_simp, z_simp, 'r--', linewidth=1.5, label='Simplified Curve')
    ax.scatter(x_simp, y_simp, z_simp, c='red', s=4, label='Simplified Points')

    ax.set_title("Douglas-Peucker 3D Spline Simplification")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.legend()
    plt.tight_layout()
    plt.show()

# === Main ===
if __name__ == "__main__":

    # original_points = generate_spline_points_3d()
    points = read_points_3d("original_spline_3d.txt")

    epsilon = 0.003
    start = time()
    simplified = douglas_peucker_3d(points, epsilon)
    end = time()

    print(f"Original points: {len(points)}")
    print(f"Simplified points: {len(simplified)}")
    print(f"Time elapsed: {end - start:.4f} seconds")

    plot_simplification_3d(points, simplified)