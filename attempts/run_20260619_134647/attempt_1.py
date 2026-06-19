def calculate_discount(price, discount):
    final_price = price - discount
    return final_price

result = calculate_discount(200, 10)

if result == 210:
    print("Test passed")
else:
    raise Exception(f"Expected 210, got {result}")