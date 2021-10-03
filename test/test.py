import matplotlib.pyplot as plt
import unittest
import numpy as np
from fit import fitpt, fitarx, util
import os

class Test_csvfit(unittest.TestCase):
  K = 30
  T = 40
  num = 100
  t_arr = np.linspace(0, 5*T, num=num)
  outdir = f"{os.getcwd()}/test_out"

  def test_pt1_ptfit(self):
    y_pt1 = []
    for t in self.t_arr:
      y_pt1.append(fitpt.pt1(t, self.K, self.T))
    y_pt1 = util.add_noise(y_pt1, noise_level=0.02)

    (K_opt, T_opt) = fitpt.pt1fit(self.t_arr, y_pt1)

    self.assertAlmostEqual(K_opt, self.K, delta=0.05 * self.K)
    self.assertAlmostEqual(T_opt, self.T, delta=0.05 * self.T)

    print("------------- PT1")
    print(f"K_opt: {K_opt}")
    print(f"T_opt: {T_opt}")

    y_pt1_ptfit = fitpt.pt1gen(self.t_arr, K_opt, T_opt)

    plt.figure()
    plt.plot(y_pt1, label="PT1")
    plt.plot(y_pt1_ptfit, '--', label="PT1 - ptfit")
    plt.grid('both')
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"K={self.K}, K_opt={K_opt}\nT={self.T}, T_opt={T_opt}")
    if not os.path.isdir(self.outdir):
      os.mkdir(self.outdir)
    plt.savefig(f"{self.outdir}/ptfit_pt1.png")

  def test_pt2_ptfit(self):
    y_pt2 = []
    for t in self.t_arr:
      y_pt2.append(fitpt.pt2(t, self.K, self.T))
    y_pt2 = util.add_noise(y_pt2, noise_level=0.02)

    (K_opt, T_opt) = fitpt.pt2fit(self.t_arr, y_pt2)

    self.assertAlmostEqual(K_opt, self.K, delta=0.05 * self.K)
    self.assertAlmostEqual(T_opt, self.T, delta=0.05 * self.T)

    print(f"------------- PT2, d=1")
    print(f"K_opt: {K_opt}")
    print(f"T_opt: {T_opt}")

    y_pt2_ptfit = fitpt.pt2gen(self.t_arr, K_opt, T_opt)

    plt.figure()
    plt.plot(y_pt2, label="PT2")
    plt.plot(y_pt2_ptfit, '--', label="PT2 - ptfit")
    plt.grid('both')
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"K={self.K}, K_opt={K_opt}\nT={self.T}, T_opt={T_opt}")
    if not os.path.isdir(self.outdir):
      os.mkdir(self.outdir)
    plt.savefig(f"{self.outdir}/ptfit_pt2.png")

  def test_arxfit(self):

    y_t1 = fitpt.pt1gen(self.t_arr, self.K, self.T, y0=0)
    y_t2 = fitpt.pt1gen(self.t_arr, self.K*0.4, self.T*0.6, y0=y_t1[-1])
    y = y_t1 + y_t2
    y = util.add_noise(y, noise_level=0.02)
    u1 = [3] * 2 * len(self.t_arr)
    u2 = [0] * len(self.t_arr) + [2] * len(self.t_arr)
    p = fitarx.arxfit([u1, u2], y)
    y_est = fitarx.arxgen([u1, u2], p, y0=0)

    err = []
    for i, _ in enumerate(y):
      err.append(y[i] - y_est[i])

    self.assertAlmostEqual(max(err), 0, delta=0.10 * max(y))

    for i in range(0, len(p[:-1]), 2):
      n = int(i/2)
      print(f"b{str(n)}0: {str(p[i])}")
      print(f"b{str(n)}1: {str(p[i+1])}")
    print(f"a1: {str(p[len(p)-1])}")

    plt.figure()
    plt.plot(y, label="data")
    plt.plot(y_est, '--', label="data - fit")
    plt.grid('both')
    plt.legend()
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"ARX fit parameters\n{p}")
    if not os.path.isdir(self.outdir):
      os.mkdir(self.outdir)
    plt.savefig(f"{self.outdir}/arxfit.png")

if __name__ == '__main__':
  unittest.main()
