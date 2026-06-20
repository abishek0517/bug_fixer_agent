def find_largest(numbers):
    largest = max(numbers)
    return largest

# === TESTS ===

test_cases = [
    ([2, 9, 4], 9),
    ([-8, -2, -5], -2),
    ([7], 7)
]

for numbers, expected in test_cases:
    result = find_largest(numbers)

    if result != expected:
        raise Exception(
            f"For {numbers}, expected {expected}, got {result}"
        )

print("All tests passed")