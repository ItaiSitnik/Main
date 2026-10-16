from itertools import combinations


def grid_to_string(grid):
    """Convert a grid to a string representation."""
    return "\n".join(
        ["".join(["🟦" if cell else "⬜" for cell in row]) for row in grid]
    )


def generate_rotations_and_reflections(grid):
    """Generate all rotations and reflections of an n x n grid."""
    grids = []
    size = len(grid)
    # Rotations
    for _ in range(4):
        grids.append(grid)
        grid = [list(row) for row in zip(*grid[::-1])]
    # Reflections (horizontal and vertical)
    grids.append([row[::-1] for row in grid])  # Horizontal
    grids.append(grid[::-1])  # Vertical
    return grids


def is_unique(grid, unique_grids):
    """Check if a grid is unique among the given unique grids."""
    for unique in unique_grids:
        if grid in generate_rotations_and_reflections(unique):
            return False
    return True


def count_unique_arrangements(n):
    """Count unique seating arrangements for 0 to n^2 people in an n x n grid."""
    results = {}
    total_seats = n * n

    for num_people in range(total_seats + 1):  # 0 to n^2 people
        all_positions = list(combinations(range(total_seats), num_people))
        unique_grids = []

        for positions in all_positions:
            grid = [[0 for _ in range(n)] for _ in range(n)]
            for pos in positions:
                grid[pos // n][pos % n] = 1

            if is_unique(grid, unique_grids):
                unique_grids.append(grid)

        results[num_people] = unique_grids
    return results


def display_results(results, only_counts=False):
    """Display results with 🟦 for seated and ⬜ for empty, or only counts."""
    for num_people, grids in results.items():
        if only_counts:
            print(f"Number of people: {num_people}, Unique arrangements: {len(grids)}")
        else:
            print(f"Number of people: {num_people}")
            for grid in grids:
                print(grid_to_string(grid))
                print()  # Separate grids


only_counts = True
for n in range(1, 6):
    print(f"> {n = }")
    results = count_unique_arrangements(n)
    display_results(results, only_counts)
    print(f"\n")
