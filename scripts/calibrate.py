import matplotlib as mpl

fsize = 12
mpl.rcParams['legend.fontsize'] = fsize-2
mpl.rcParams['axes.titlesize'] = fsize+2
mpl.rcParams["figure.figsize"] = (6.47, (6.47*9)/20)
mpl.rcParams['axes.labelsize'] = fsize
mpl.rcParams['xtick.labelsize'] = fsize
mpl.rcParams['ytick.labelsize'] = fsize
mpl.rcParams['text.usetex'] = True
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['mathtext.fontset'] = 'dejavusans'
mpl.rcParams.update({'font.size': fsize})

from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np
import random as rn
from scipy import interpolate

import linealization

cols = 8

dV1 = 2 #mV
dV2 = 10 #mV
Voltages = list(range(12, 41, dV1))+list(range(50, 151, dV2))+list(range(170, 231, dV2))
iterations = len(Voltages)

repetitions = 100

tot_events = iterations*repetitions

data = np.genfromtxt('../data/wide_range_calibration.txt', skip_header=1, dtype="int")

data.T[4:] = (data.T[4:]/16).astype(int)

max_Voltage = data.T[4].max()
print(max_Voltage)

min_Voltage = data.T[-1].min()
print(min_Voltage)

max_time = data.T[3].max()
print(max_time)

print(data)

color = cm.rainbow(np.linspace(0, 1, iterations))
print(color)
a0_list = [None]*repetitions
a1_list = [None]*repetitions

a0_err_list = [None]*repetitions
a1_err_list = [None]*repetitions

x = np.arange(0, 140, 0.1)

#get average
A0 = [0]*iterations
S0 = [0]*iterations
repeat = list()
for i in range(iterations):
    data_sample = data.T[4][i*repetitions:(i+1)*repetitions]
    A0[i] = np.mean(data_sample)
    S0[i] = np.std(data_sample)

    min_val = data_sample.min()
    max_val = data_sample.max()

    if min_val < A0[i]-3*S0[i] or max_val > A0[i]+3*S0[i]:
        repeat.append(Voltages[i])

print("repeat:", repeat)

for i in range(iterations):

    sum_a0_1 = 0
    sum_a0_2 = 0

    sum_a1_1 = 0
    sum_a1_2 = 0

    label = None

    for r in range(0,repetitions):

        sum_a0_1 = 0
        sum_a0_2 = 0

        sum_a1_1 = 0
        sum_a1_2 = 0

        '''t0 = data[i*repetitions+r][2]
        times = [0]+[t for t in data[i*repetitions+r][3:7]]
    
        #ADC_Error = [200]*repetitions
        ADC_Error = [rn.randint(400, 1000) for i in range(repetitions)]
        X = [0]+[t for t in data[i*repetitions+r][3:7]]
        Y = [np.log(y) for y in data[i*repetitions+r][7:]]
        a0, a1, err_a0, err_a1, chi2 = linealization.adjust(X, Y, ADC_Error)

        a0 = np.exp(a0)
        err_a0 = err_a0*a0

        a0_list[r] = a0
        a1_list[r] = a1

        a0_err_list[r] = err_a0
        a1_err_list[r] = err_a1

        sum_a0_1 += a0/err_a0**2
        sum_a0_2 += 1/err_a0

        sum_a1_1 += a1/err_a1**2
        sum_a1_2 += 1/err_a1'''

        t0 = 0
        dt = data[i*repetitions+r][3]/4

        times = [i*dt for i in range(5)]

        plt.plot(times, data[i*repetitions+r][4:], color=color[i], linewidth=0.5)

    '''y_list = [list()]*repetitions
    for j in range(repetitions):
        y_list[j] = [a0_list[j]*np.exp(a1_list[j]*xj) for xj in x]
    
    y = [sum(val)/repetitions for val in zip(*y_list)]
    A0[i] = y[0]

    plt.plot(x, y, color="black", linewidth=1.0)'''

    #label_y_pos = (i+1)*(max_Voltage-min_Voltage)/iterations
    #print(label_y_pos)

    plt.text(x=max_time-2, y=A0[i], s=str(data[i*repetitions][0]), color=color[i])

#plt.yscale(value="log")

plt.grid()

plt.xlabel("Time [us]")
plt.ylabel("ADC reading")

plt.text(x=max_time-40, y=max_Voltage, s="Signal Amplitude [mV]")

plt.savefig("../figures/decays2.pdf", bbox_inches="tight")
plt.clf()

print(Voltages)
print(A0)

def f(x):
    tck = interpolate.splrep(Voltages, A0)
    return interpolate.splev(x, tck)

#S0[0] = S0[0]/1000.
fit = np.polyfit(x=Voltages, y=A0, deg=11, w=S0)
print(fit)

p = np.poly1d(fit)

X = np.arange(0, max(Voltages), 0.5)
Y = [p(x) for x in X]

container = plt.errorbar(Voltages, A0, yerr=S0, fmt="o", markersize=1, label="measured data", lw=0.5)
plt.plot(X, Y, label="polynomial fit")
#plt.scatter(Voltages, A0, c=color)

#plt.yscale(value="log")
plt.xlabel("Pulse amplitude [mV]")
plt.ylabel("ADC reading [channel]")

plt.ylim(bottom=1)
plt.grid()

plt.legend(loc="upper left")

plt.savefig("../figures/ADC_to_amplitude2.pdf", bbox_inches="tight")