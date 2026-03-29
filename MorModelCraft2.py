## CRAFT model based on code by
## Greg O'Donnell, CRAFTQ2 (lagged store) coded by Russell Adams
## 1st June 2016

import pylab
import csv
import dateutil.parser as parser
from scipy.optimize import minimize

def simplex(par):
    flow = craftq2(par)
    ns = nash_sutcliffe(flow)
    print('Parameters',par)
    print('E', ns)
    return -ns # minimising

def craftq2(par):
#    sdmax = par[0]
#    ksurf = par[1]
#    klag = par[2]
#    kss = par[3]
#    kg=par[4]
#    srmax=par[5]
#    split=par[6]

    sms = 0.3*par[5]
    ss = surfs = sroute = 0.0
    sgw = 20.0
    qsr = drain = 0.0
    
    flow = []

    for i in range(len(date)):
        surfs = surfs + r[i] - qsr - drain
        surfs = max(0,surfs) 
        drain = min(par[0],surfs)
        qsr = max(0,(surfs-drain)*par[1])
        sms = max(0,sms+drain-ae[i])
        if sms>par[5]:
           perc = sms-par[5]
           sms = par[5]
        else:
           perc =0
           
        qss = ss * par[3]
        ss = max(0,ss+par[6]*perc-qss)
        qgw = sgw * par[4]
        sgw = max(0,sgw+(1-par[6])*perc-qgw)
# route surface runoff through lagged store
        par[2] = max(0,par[2])
        qsrlag = sroute*(1-par[2])
        sroute=  max(0,sroute-qsrlag+qsr)
# add flows together        
        flow.append(qsrlag+qss+qgw)

    return flow


def nash_sutcliffe(flow):
    num = 0
    den = 0
    avg = sum(flow)/len(flow)
    for i in range(len(q)):
        num = num + (q[i]-flow[i])**2
        den = den + (q[i]-avg)**2

    ns = 1-num/den
    return ns

    
#################################################################


date = []
q = []
r = []
ae = []
with open('Morland1112ObsDataQ.csv') as csvfile:
    rdr = csv.reader(csvfile)
    next(rdr) # skip header
    for row in rdr:
        date.append(parser.parse(row[0],dayfirst=True))      
        r.append(float(row[1]))
        ae.append(float(row[2]))
        q.append(float(row[3]))


print('Q, R, AE', sum(q), sum(r), sum(ae))


par = [5.0,0.5,0.8,0.01,0.001,40.0,0.5]

res = minimize(simplex, par, method='nelder-mead',options={'maxiter': 1000, 'disp': True})
par = res['x']

flow = craftq2(par)
ns = nash_sutcliffe(flow)
print('Nash & Sutcliffe', ns)
print('Parameters', res['x'])


fig = pylab.figure(figsize=(10,6))

ax1=fig.add_subplot(111)        
ax1.plot(date,q,c='k')
ax1.plot(date,flow,c='r')
ax1.set_ylim(0,4)
ax1.set_ylabel('mm/hr')

ax2 = ax1.twinx()
ax2.plot(date,r,c='b')
ax2.set_ylim(10,0)
ax2.set_ylabel('mm/hr')

pylab.show()
