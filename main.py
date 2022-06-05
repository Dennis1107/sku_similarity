from sku_similarity.sku_similarity_input import input_checker_functions as icf
from sku_similarity.sku_similarity_calculation import calculate_sku_similarity as css

default_number_sku = 10
default_sku = "sku-123"

print("Hello Thorsten, Matjea & Team \U0001F680")

input_sku = input(f"Enter sku code (default is {default_sku}): ") or f"{default_sku}"
input_number_sku = (
    input(f"Number of similar skus (default is {default_number_sku}): ")
    or f"{default_number_sku}"
)

sku_code = icf.apply_input_checking(input_sku)
similarity_data = css.apply_similarity_calculation(sku_code, input_number_sku)
print(f"Here are the top {input_number_sku} similar skus: ")
print(similarity_data)
