from click.testing import CliRunner
from pyxor.pyxor import extract_yaml_value

def test_extract_yaml_value_stdin():
  runner = CliRunner()
  result = runner.invoke(extract_yaml_value, ["--expr", "root.child.text", "--file", "-"], input='root:\n    child:\n        text: test')
  print(result.output)
  assert result.output == "['test']\n"
  assert result.exit_code == 0

def test_extract_yaml_value_file():
  runner = CliRunner()
  
  with runner.isolated_filesystem():
      with open('test.yaml', 'w') as f:
          f.write('root:\n    child:\n        text: test')
  
      result = runner.invoke(extract_yaml_value, ["--expr", "root.child.text", "--file", "test.yaml"])
      assert result.output == "['test']\n"
      assert result.exit_code == 0
