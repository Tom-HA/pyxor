from jsonpath_rw import parse, lexer
from yaml import safe_load, YAMLError

def extract_values_from_yaml(stream, expression):
    try:
        data = safe_load(stream)
    except YAMLError as e:
        raise e
    try:
        jsonpath_expr = parse(expression)
    except lexer.JsonPathLexerError as e:
        raise e
    
    values = []
    for match in jsonpath_expr.find(data):
        values.append(match.value)
    if len(values) == 1:
        return {"data": values[0]}
    
    return {"data": values}