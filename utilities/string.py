import re


def extract_number_from_string(input_string: str) -> float:
  """
  Extracts the first number from a given string and returns it as a float.
  
  Args:
    input_string (str): The string from which to extract the number.
    
  Returns:
    float: The first extracted number as a float, or 0.0 if not found.
  """
  # Replace comma with dot for decimal separator
  normalized = input_string.replace(',', '.')
  match = re.search(r"[-+]?\d*\.\d+|[-+]?\d+", normalized)
  if match:
    return float(match.group())
  return 0.0
