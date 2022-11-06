#!/usr/bin/env python3
import sys
import click
import os
import logging
from jsonpath_rw.lexer import JsonPathLexerError
from yaml import YAMLError
from internal import parser

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%(levelname)s:\t\t%(message)s')

@click.command()
@click.option('--expr', '-e', type=str, required=True, help='The expression to extract')
@click.option('--file', '-f',
              type=click.File(mode='r'),
              required=True,
              help='The name of a yaml file. If the file path is `-`, then the YAML content is read from stdin')
    
def extract_yaml_value(file: str, expr: str):
    with file:
        try:
            data = file.read()
        except Exception as e:
            print(e)
    try:
        values = parser.extract_values_from_yaml(data, expr)
    except YAMLError as e:
        logging.debug(e)
        print("Failed to parse YAML")
        sys.exit(1)
    except JsonPathLexerError as e:
        logging.debug(e)
        print("Failed to parse YAML path expression")
        sys.exit(1)
    except AttributeError as e:
        logging.debug(e)
        print(e)
        sys.exit(1)
    except Exception as e:
        logging.debug(e)
        print("Unhandled error")
        sys.exit(1)
        
    print(values)

if __name__ == '__main__':
    extract_yaml_value()