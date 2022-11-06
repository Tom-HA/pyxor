from jsonpath_rw import parse
from yaml import safe_load

def extract_values_from_yaml(stream, expression):
    data = safe_load(stream)
    jsonpath_expr = parse(expression)
   
    values = []
    for match in jsonpath_expr.find(data):
        values.append(match.value)

    if len(values) == 1:
        return {"data": values[0]}
    
    return {"data": values}