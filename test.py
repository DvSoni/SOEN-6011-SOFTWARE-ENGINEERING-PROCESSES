from beta_function_scratch import real_power, my_ln, UnsupportedDomainError, UndefinedOperationError

try:
    real_power(-2.0, 3.0)
except UnsupportedDomainError as e:
    print("Caught:", e)

try:
    my_ln(0.0)
except UndefinedOperationError as e:
    print("Caught:", e)