import numpy as np
import matplotlib.pyplot as plt
import math
from time import time

# === Generate Spline ===
def generate_spline_points(
    filename="original_spline.txt",
    num_points=10000,
    x_range=(0, 10),
    y_scale=1.0,
    show_graph=False,
    random_seed=42
):
    np.random.seed(random_seed)
    x = np.linspace(x_range[0], x_range[1], num_points)

    y = (
        0.1 * x**3
        - 1.0 * x**2
        + np.sin(1.5 * x) * np.exp(-0.08 * x)
        + 0.35 * np.tanh(8 * np.cos(0.625 * x))
        + 0.5 * np.sin(3 * x + 0.5 * np.cos(0.75 * x))
        + 0.3 * np.sin(5 * x)
        + 0.15 * np.sin(13 * x + np.sin(7 * x))
        + 0.1 * np.arctan(np.sin(6 * x) * np.cos(4 * x))
        + 0.05 * np.random.uniform(-1, 1, size=x.shape)
    )

    y_centered = y - np.mean(y)
    y_scaled = (y_centered / np.max(np.abs(y_centered))) * y_scale

    if show_graph:
        plt.figure(figsize=(10, 5))
        plt.plot(x, y_scaled, linewidth=1)
        plt.title("Chaotic Spline Curve")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    with open(filename, "w") as f:
        for x_val, y_val in zip(x, y_scaled):
            f.write(f"{x_val},{y_val}\n")

    print(f"Text file '{filename}' saved with {num_points} points.")
    return [(float(x_val), float(y_val)) for x_val, y_val in zip(x, y_scaled)]

# === Read Points ===
def read_points(filename):
    with open(filename, 'r') as f:
        return [tuple(map(float, line.strip().split(','))) for line in f]

# === Perpendicular Distance Helper ===
def perpendicular_distance(pt, line_start, line_end):
    x, y = pt
    x1, y1 = line_start
    x2, y2 = line_end

    if (x1 == x2) and (y1 == y2):
        return math.dist(pt, line_start)

    dx = x2 - x1
    dy = y2 - y1
    t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx*dx + dy*dy)))

    closest_x = x1 + t * dx
    closest_y = y1 + t * dy

    return math.dist(pt, (closest_x, closest_y))

# === Douglas-Peucker Algorithm ===
def douglas_peucker(points, epsilon):
    start, end = points[0], points[-1]

    max_dist = 0
    index = 0
    for i in range(1, len(points) - 1):
        dist = perpendicular_distance(points[i], start, end)
        if dist > max_dist:
            max_dist = dist
            index = i

    if max_dist > epsilon:
        left = douglas_peucker(points[:index+1], epsilon)
        right = douglas_peucker(points[index:], epsilon)
        return left[:-1] + right
    else:
        return [start, end]

# === Plot Function ===
def plot_simplification(original, simplified):
    plt.figure(figsize=(12, 7))
    x_orig, y_orig = zip(*original)
    x_simp, y_simp = zip(*simplified)

    plt.plot(x_orig, y_orig, 'k-', linewidth=1, label='Original')
    plt.plot(x_orig, y_orig, 'ko', markersize=2, label='Original Points')

    plt.plot(x_simp, y_simp, 'r--', linewidth=1.5, label=f'Douglas-Peucker Line ({len(simplified)} pts)')
    plt.plot(x_simp, y_simp, 'ro', markersize=4, label='Simplified Points')

    plt.title("Douglas-Peucker Spline Simplification")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# === Main ===
if __name__ == "__main__":
    filename = "original_spline.txt"
    num_points = 100_000
    show_graph = False

    original_points = generate_spline_points()

    points = read_points(filename)

    epsilon = 0.02
    start = time()
    simplified = douglas_peucker(points, epsilon)
    end = time()

    print(f"Original points: {len(points)}")
    print(f"Simplified points: {len(simplified)}")
    print(f"Time elapsed: {end - start:.4f} seconds")

    plot_simplification(points, simplified)