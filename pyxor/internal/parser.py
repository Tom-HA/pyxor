from jsonpath_rw import parse
import yaml

def extract_values_from_yaml(stream, expression):
    data = yaml.safe_load(stream)
    jsonpath_expr = parse(expression)
    values = []
    for match in jsonpath_expr.find(data):
        values.append(match.value)
    if len(values) == 1:
        return values[0]
    
    return values