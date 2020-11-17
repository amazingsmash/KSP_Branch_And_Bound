import csv
from node import *

# Mirrored from Kaggle notebook at: https://www.kaggle.com/jquinteiro/ksp-l1-g0-branch-and-bound-final

# Example data for testing
example_csv = """3 10
                    45 5
                    48 8
                    35 3
                    """
example_items = [Item(index=0, value=45, weight=5),
                 Item(index=1, value=48, weight=8),
                 Item(index=2, value=35, weight=3)]
example_capacity = 10
example_value = 80
example_taken = [1, 0, 1]


def from_data_to_items(input_data):
    lines = input_data.split('\n')

    first_line = lines[0].split()
    item_count = int(first_line[0])
    capacity = int(first_line[1])

    items = []
    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1])))

    return items, capacity


def solve_naive(items, capacity):
    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0] * len(items)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    return value, taken


def solve_branch_and_bound(items, capacity):
    root_node = Node(0, [], 0, capacity)
    alive = [root_node]

    best_value = 0

    while len(alive) > 0:
        current = alive.pop()

        if current.room <= 0:
            continue

        current_estimate = current.estimate(items)

        if current_estimate <= best_value:
            continue

        if current.value > best_value:
            best_value = current.value
            best = current

        if current.index >= len(items):
            continue

        right_node = Node(current.index + 1, current.path.copy(), current.value, current.room)
        alive.append(right_node)

        left_path = current.path.copy()
        left_path.append(current.index)  # xi =0

        left_node = Node(current.index + 1,
                         left_path,
                         current.value + items[current.index].value,
                         current.room - items[current.index].weight)
        alive.append(left_node)

    taken = [0] * len(items)

    for i in best.path:
        taken[items[i].index] = 1

    return best_value, taken


if __name__ == '__main__':

    value, taken = solve_branch_and_bound(example_items, example_capacity)

    print(value)
    print(taken)
