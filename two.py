import numpy as np
import matplotlib.pyplot as plt
import random
import pandas as pd
import sys
import scipy.stats as stats


import matplotlib as mpl
mpl.rcParams["errorbar.capsize"] = 3
mpl.rcParams["lines.linewidth"] = 1
mpl.rcParams['pdf.fonttype'] = 42




np.set_printoptions( threshold=999999999999999)


def trevrolls(frates):
	r2=0.
	rs =0.
	n = float(frates.size)
	for i in range(frates.size): # np.nditer(frates):
		r2 += (frates[i]**2)/n
		rs += frates[i]/n
	return 1. - ((rs**2)/r2)
	

NPYRS = 400
NRUNS=10

def plotCase(case, title):
	for prp in ['G' ]:
		print "Case=",case

		dend_ids = [0,1]
		dend_conds = [2,3]
		dend_ticks = ['linear', 'nonlinear'];

		XLEN = len(dend_conds);

		trs = np.zeros((2, XLEN,NRUNS))



		for CLUSTERED in [0,1]:
			for did in dend_ids:
				dend_cond = dend_conds[did]

				branch_hist = [];
				for run in range(NRUNS):
					spikes = np.loadtxt( './data/%s_%d_%d_%s_%d/spikesperpattern.dat'%(case, dend_cond, CLUSTERED, prp, run), dtype=float)
					spikes = spikes[:, 0:NPYRS]

					overlap = 100.*np.sum(np.logical_and((spikes[0,:] >40.),  ( spikes[1,:] >40.) )) / NPYRS

					trs[CLUSTERED, did, run] = overlap;
					"""
					syns = np.loadtxt('./data/two_%d_%d_%s_%d/syn-post.txt'%(dend_cond, CLUSTERED, prp, run), dtype=float)
					syns = syns[syns[:,4]>0.7]
					cols = ['input_id', 'group_id', 'branch_id','nid','weight']
					table = pd.DataFrame(syns,columns=cols)
					totals = table.groupby(['branch_id'])['weight'].count().values
					#branch_hist.extend(totals.tolist())

					ratio_clustered[did, run] = sum(totals>2) / float(sum(totals>0))
					"""

				#plt.figure()
				#plt.title('Synapses per branch cond=%d'%(dend_cond));
				#df = pd.DataFrame(np.array(branch_hist), columns=['cnt'])
				#df['cnt'].value_counts().plot(kind='bar')
				#plt.ylim(ymin=0)
				#plt.xticks(np.arange(4), ['supra', 'sub', 'linear', 'mixed']);	





		xr = np.arange(XLEN)

		#plt.title('case=%s'%(case));
		#trs = trs[2:3, :];
		#print( stats.f_oneway( trs[0,:] , trs[1,:] ) )

		tr_means = np.mean(trs, 1)
		tr_std =  np.std(trs,1)

		plt.bar(xr-.2, np.mean(trs[0], 1), yerr=np.std(trs[0],1), width=.3 )
		plt.bar(xr+.2, np.mean(trs[1], 1), yerr=np.std(trs[1],1), width=.3 )
		plt.ylim(ymin=0, ymax=50)
		plt.xticks(np.arange(XLEN), dend_ticks);
		plt.ylabel('Overlap (%)');
		plt.title(title)

plt.figure()
plt.subplot(1,2,1)
plotCase("two", "1 hour separation")
plt.subplot(1,2,2)
plotCase("two1440", "24h separation")
plt.savefig("mem2.pdf")

plt.show();

