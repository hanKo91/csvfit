from click.exceptions import FileError
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from . import util
import numpy as np
import click
import sys
import csv


def arxfit(u, y):
  """ARX fit of MISO system, 1.Order fit

  Args:
    u (list(list(float))): inputs [[u0], [u1], ..., u[N]]
    y (list(float)): output[y]

  Returns:
    list(float): parameters\n
    [b00, b01, b10, b11, ..., bN0, bN1, a1]
  """
  X = []
  for k in range(len(u[0]) - 1):
    X_k = []
    for u_k in u:
      X_k.append(u_k[k+1])
      X_k.append(u_k[k])
    X_k.append(y[k])
    X.append(X_k)

  X_inv = np.linalg.pinv(X)
  return np.dot(X_inv, y[1:])

def arxgen(u, p, y0=0):
  """ARX algorithm, of MISO system
  with N inputs and 1 output, 1.Order fit

  Args:
    u (list(list(float)): system inputs [[u0], [u1], ..., u[N]]
    y0 (float): initial output state
    p (list(list(float))): arx parameter\n
    [b00, b01, b10, b11, ..., bN0, bN1, a1]

  Returns:
    list(float): system outputs
  """
  y = [0] * (len(u[0]) + 1)
  y[0] = y0
  for k in range(1, len(u[0])):
    y[k] = p[len(p)-1] * y[k-1] + y[0]
    for n in range(len(u)):
      i = n * 2
      y[k] += p[i] * u[n][k] + p[i+1] * u[n][k-1]
    
  return y[:-1]

@click.option("--datapath", "-d", help="Path to csv file with target data", type=click.Path(exists=True))
@click.option("--outdir", "-o", help="Directory to store output artifacts", type=click.Path(exists=True))
@click.option("--columns", "-c", help="Name of the columns, last one is by default the system output", type=str, multiple=True)
@click.option("--show", "-s", help="Show plots", is_flag=True)
@click.command()
def do_fit(datapath, outdir, columns, show):

  data = []
  delimiter = util.get_delimiter(datapath)
  with open(datapath, 'r') as data_file:
    reader = csv.DictReader(data_file, delimiter=delimiter)
    for entry in reader:
      data.append(entry)

  u = []
  for col in columns[:-1]:
    u.append(util.column(data, col))

  y = util.column(data, columns[-1])
  arx_param = arxfit(u, y)

  for i in range(0, len(arx_param[:-1]), 2):
    n = int(i/2)
    print(f"b{str(n)}0: {str(arx_param[i])}")
    print(f"b{str(n)}1: {str(arx_param[i+1])}")
  print(f"a1: {str(arx_param[len(arx_param)-1])}")

  plt.figure()
  plt.plot(arxgen(u, 0, arx_param), label=f"{columns[-1]} --fit")
  plt.plot(util.column(data, "offset"))

def main():
  if len(sys.argv) == 1:
    do_fit.main(["--help"])
  else:
    do_fit.main()

if __name__ == "__main__":
  main()
