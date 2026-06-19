def calculate_discount(price, discount):
    final_price = price - (discount / 100)
    return final_price

result = calculate_discount(200, 10)

if result == 190:
    print("Test passed")
else:
    raise Exception(f"Expected 190, got {result}")