from jsonpath_rw import jsonpath, parse
import yaml

def extract_values_from_yaml(stream, expression):
    try:
        data = yaml.safe_load(stream)
        jsonpath_expr = parse(expression)
        values = []
        for match in jsonpath_expr.find(data):
            values.append(match.value)
        return values
    except yaml.YAMLError as e:
        print(e)
        return e