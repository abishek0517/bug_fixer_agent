def calculate_discount(price, discount):
    final_price = price - (price * discount / 100)
    return final_price

result = calculate_discount(200, 10)

if result == 180:
    print("Test passed")
else:
    raise Exception(f"Expected 180, got {result}")