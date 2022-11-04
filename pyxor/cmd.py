import click
from parser import parser

@click.command()
@click.option('--expr', '-e', type=str, required=True, help='The expression to extract')
@click.option('--file', '-f',
              type=click.File(mode='r'),
              required=True,
              help='The name of a yaml file. If the file path is `-`, then the YAML content is read from stdin')
    
def extract_yaml_value(file, expr):
    with file:
        try:
            data = file.read()
        except Exception as e:
            print(e)
    values = parser.extract_values_from_yaml(data, expr)

    print(values)

if __name__ == '__main__':
    extract_yaml_value()