from click.exceptions import FileError
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from . import util
import numpy as np
import click
import sys
import csv
import os

def pt1(t, K, T):
  """ time-domain solution/formula for
  a first-order/pt1 system

  Args:
    t (float): time
    K (float): gain
    T (float): time-constant

  Returns:
    float: f(t)
  """
  return K * (1 - np.exp(-t/T))

def pt2(t, K, T):
  """ time-domain solution/formula for
  a second-order/pt2 system with
  critical damping, d = 1, T = T1 = T2

  Args:
    t (float): time
    K (float): gain
    T (float): time-constant

  Returns:
      float: f(t)
  """
  return K * (1 - np.exp(-t/T) - ((t/T) * np.exp(-t/T)))

def pt1gen(t_arr, K, T, y0 = 0):
    """ generate y(t) of PT1 for t in t_arr

    Args:
      t_arr (list(float)): time array
      K (float): gain
      T (float): time-constant

    Returns:
      list(float): y(t) for t in t_arr
    """
    return [pt1(t, K, T) + y0 for t in t_arr]

def pt2gen(t_arr, K, T, y0 = 0):
  """ generate y(t) of PT2 for t in t_arr

  Args:
    t_arr (list(float)): time array
    K (float): gain
    T (float): time-constant

  Returns:
    list(float): y(t) for t in t_arr
  """
  return [pt2(t, K, T) + y0 for t in t_arr]

def pt1fit(t, y, Kg=1, Tg=1):
  """ curve_fit of pt1(-like) data

  Args:
    t (list(float)): time
    y (list(float)): output
    Kg (float, optional): initial guess for gain. Defaults to 1.
    Tg (float, optional): initial guess for time-constant. Defaults to 1.

  Returns:
    tuple(float,float): best fit -> K_opt, T_opt
  """

  if not len(t) == len(y):
    return None

  # delete offset and normalize
  t = [n - t[0] for n in t]
  y = [n - y[0] for n in y]
  t_norm = [n / max(t) for n in t]
  y_norm = [n / max(y) for n in y]

  (popt,_) = curve_fit(pt1, t_norm, y_norm, p0=[Kg, Tg], absolute_sigma=True)

  K_opt = max(y) * popt[0]
  T_opt = max(t) * popt[1]
  return (K_opt, T_opt)

def pt2fit(t, y, Kg=1, Tg=1):
  """ curve_fit of pt2(-like) data
  
  Args:
    t (list(float)): time
    y (list(float)): output
    Kg (float, optional): initial guess for gain. Defaults to 1.
    Tg (float, optional): initial guess for time-constant. Defaults to 1.

  Returns:
    tuple(float,float): best fit -> K_opt, T_opt
  """
  if not len(t) == len(y):
      return None

  # delete offset and normalize
  t = [n - t[0] for n in t]
  y = [n - t[0] for n in y]
  t_norm = [n / max(t) for n in t]
  y_norm = [n / max(y) for n in y]

  (popt,_) = curve_fit(pt2, t_norm, y_norm, p0=[Kg, Tg], absolute_sigma=True)

  K_opt = max(y) * popt[0]
  T_opt = max(t) * popt[1]
  return (K_opt, T_opt)

@click.option("--datapath", "-d", help="Path to csv file with target data", type=click.Path(exists=True))
@click.option("--eventspath", "-e", help="Path to csv file with event data", type=click.Path())
@click.option("--outdir", "-o", help="Directory to store output artifacts", type=click.Path(exists=True))
@click.option("--columns", "-c", help="Name of the columns", type=str, multiple=True)
@click.option("--type", "-t", help="PTn type: PT1, PT2", type=str, multiple=True)
@click.option("--show", "-s", help="Show plots", is_flag=True)
@click.command()
def do_fit(datapath, eventspath, outdir, columns, show):

  data = []
  delimiter = util.get_delimiter(datapath)
  with open(datapath, 'r') as data_file:
    reader = csv.DictReader(data_file, delimiter=delimiter)
    for entry in reader:
      data.append(entry)

  events = []
  delimiter = util.get_delimiter(eventspath)
  with open(eventspath, 'r') as events_file:
    reader = csv.DictReader(events_file, delimiter=delimiter)
    for entry in reader:
      events.append(entry)

    data_per_event = {}
    time_slots = []
    for key in list(events[0].keys()):
      if key == "<event-name>":
        continue
      from_index = int(events[0][key])
      to_index = int(events[1][key])
      time_slots.append(range(from_index, to_index))
      data_per_event[key] = data[from_index:to_index]

  for col in columns:
    ptn_param = []
    plt.figure()
    plt.plot(util.column(data, col), label="all")
    for index, key in enumerate(list(data_per_event.keys())):
      if type == "PT1":
        ptn_param.append(pt1fit(time_slots[index], util.column(data_per_event[key], col)))
      elif type == "PT2":
        ptn_param.append(pt2fit(time_slots[index], util.column(data_per_event[key], col)))
      
      print(key, end=": (K_opt, T_opt)=")
      print(ptn_param[index])
      plt.plot(time_slots[index], util.column(data_per_event[key], col), label=f"{key} : {time_slots[index]}")
      plt.legend()
      plt.grid('both')
      plt.savefig(f"{outdir}/timeslots_{col}.png")

    for index, key in enumerate(list(data_per_event.keys())):
      plt.figure()
      col_data = np.array(util.column(data_per_event[key], col))
      col_data -= col_data[0]
      plt.plot(col_data, label=f"{key}")
      t_arr = range(len(time_slots[index]))
      K_opt = ptn_param[index][0]
      T_opt = ptn_param[index][1]
      if type == "PT1":
        plt.plot(pt1gen(t_arr, K_opt, T_opt), "--", label=f"{key} --fit")
      elif type == "PT2":
        plt.plot(pt2gen(t_arr, K_opt, T_opt), "--", label=f"{key} --fit")
        plt.title(f"K_opt: {K_opt}\nT_opt: {T_opt}")
        plt.legend()
        plt.grid('both')
        plt.savefig(f"{outdir}/{col}_{key}_fit.png")

  if show:
    plt.show()

def main():
  if len(sys.argv) == 1:
    do_fit.main(["--help"])
  else:
    do_fit.main()

if __name__ == "__main__":
  main()

