def calculate_discount(price, discount):
    final_price = price - int(discount)
    return final_price

result = calculate_discount(200, 10)

if result == 190:
    print("Test passed")
else:
    raise Exception(f"Expected 190, got {result}")