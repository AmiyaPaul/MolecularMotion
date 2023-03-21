import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import rc
rc('animation',html='jshtml')

# Parameter

b_x = 1000
b_y = 1000
n = 500
m = 1e-5
sig = 10
ep = 2
max_speed = 50
t = 0.5

# function

def acc(r,a=sig,b=ep,c=m):
  kl = np.zeros(len(r))
  for i in range(len(r)):
    k = a/r[i]
    f = -48*b*(k**6)*((k**6)-0.5)/r[i]
    if abs(r[i]) >= 30:
      kl[i] = 0
    elif abs(r[i]) <= a*2:
      if r[i] < 0:
        kl[i] = 0.5
      else:
        kl[i] = -0.5
    else:
      kl[i] = f
  return kl

def acset(pos1,acc):
  acse = np.zeros(n)
  for i in range(n):
    rx = np.zeros(n)
    for j in range(n):
      rxn = pos1[j] - pos1[i]
      rx[j] = rxn
    rx = np.delete(rx,i)
    accn = acc(rx)
    acse[i] = sum(accn)
  return acse

# Initialisation

p_x = np.random.rand(n)*(b_x-20)
p_y = np.random.rand(n)*(b_y-20)
v_x = (np.random.rand(n)-0.5)*max_speed
#v_x = np.zeros(n)
v_y = (np.random.rand(n)-0.5)*max_speed
#v_y = np.zeros(n)

for h in range(n):
  p_x[h] = round(p_x[h],2)
  p_y[h] = round(p_y[h],2)
  v_x[h] = round(v_x[h],2)
  v_y[h] = round(v_y[h],2)

# Run

fig, ax = plt.subplots()

def update(frame):
  a_x = acset(p_x,acc)
  a_y = acset(p_y,acc)

  for d in range(n):
    p_x[d] = p_x[d] + (v_x[d] * t) + (0.5 * a_x[d] * t * t)
    v_x[d] = v_x[d] + (a_x[d] * t)
    p_y[d] = p_y[d] + (v_y[d] * t) + (0.5 * a_y[d] * t * t)
    v_y[d] = v_y[d] + (a_y[d] * t)

    if p_x[d] >= (b_x-20):
      p_x[d] = 2*(b_x-20) - p_x[d]
      v_x[d] = -v_x[d]
    if p_y[d] >= (b_y-20):
      p_y[d] = 2*(b_y-20) - p_y[d]
      v_y[d] = -v_y[d]
    if p_x[d] <= 20:
      p_x[d] = 40 - p_x[d]
      v_x[d] = -v_x[d]
    if p_y[d] <= 20:
      p_y[d] = 40 - p_y[d]
      v_y[d] = -v_y[d]

  ax.cla()
  plt.figure(figsize=(10,10))
  plt.xlim([0,b_x])
  plt.ylim([0,b_y])
  return ax.scatter(p_x,p_y,c='black',s=20)

anim = animation.FuncAnimation(fig,update,interval=1000)
plt.show()