from click.exceptions import FileError
import numpy as np

def add_noise(y, noise_level):
  """ add noise to y (pointwise)

  Args:
    y (list(float)): input
    noise_level (float): noise_amplitude = max(y) * noise_level

  Returns:
    list(float): y + noise
  """
  noise_amplitude = noise_level * max(y)
  noise = np.random.normal(0, noise_amplitude, len(y))
  return [a + b for a, b in zip(y, noise)]

def get_delimiter(path, valid_delimiters=[',', ';']):
  """ get delimiter of csv file

  Args:
    path (str): the csv file
    valid_delimiters (list, optional): csv delimiter. Defaults to [',', ';'].

  Raises:
    FileError: if the file does not contain a valid delimiter

  Returns:
    str: delimiter found in header
  """
  with open(path, 'r') as csv_file:
    header = csv_file.readline()
    for delimiter in valid_delimiters:
      if delimiter in header:
        return delimiter
  raise FileError("Not a csv file with a valid delimiter!")

def column(data, key):
  """ get specific column

  Args:
      data (list(dict)): data object returned by csv.DictReader
      key (str): name of the column (header in first row)

  Returns:
      list(float): column data
  """
  column_data = []
  for row in data:
    column_data.append(float(row[key]))
  return column_data