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
	

def loadspikesdat(filename, tduration):

	ff = open(filename, 'r') 
	fdata = ff.readlines()
	sx = len(fdata)
	sy = tduration;
	raster = np.zeros( (sx, sy) );
	nid=0
	for l in fdata:
		ar = np.fromstring(l, sep=' ' , dtype=int)
		raster[nid, ar] = 1
		raster[nid,0] =0 # XXX bug
		nid += 1

	return raster


def printpairstats(stat, name):
	print( name)
	print( stats.f_oneway( stat[0][0] , stat[1][0] ) ) 
	print( stats.f_oneway( stat[0][1] , stat[1][1] ) )
	print( stats.f_oneway( stat[0][0] , stat[0][1] ) )
	print( stats.f_oneway( stat[1][0] , stat[1][1] ) )
	

def label_diff(ax, i,j,text,X,Y):
    x = (X[i]+X[j])/2
    y = 1.1*max(Y[i], Y[j])
    dx = abs(X[i]-X[j])
    props = {'connectionstyle':'bar','arrowstyle':'-',\
                 'shrinkA':20,'shrinkB':20,'linewidth':1}
    ax.annotate(text, xy=(X[i],y-7), zorder=10, transform=ax.transData)
    #ax.text(.5, .5, "text")
    ax.annotate('', xy=(X[i],y), xytext=(X[j],y), arrowprops=props)

NPYRS = 400
NRUNS=20
CLUSTERED=0



for prp in ['G' ]:

	dend_ids = [0,1]
	dend_conds = [2,3]
	dend_ticks = ['Linear', 'Nonlinear'];

	XLEN = len(dend_conds);

	trs = np.zeros((2, XLEN,NRUNS))
	ffs = np.zeros((2, XLEN,NRUNS));
	pops = np.zeros((2, XLEN,NRUNS));
	ratio_clustered = np.zeros((2, XLEN,NRUNS));

	for CLUSTERED in [0,1]:
		print "PRP=",prp


		for did in dend_ids:
			dend_cond = dend_conds[did]

			branch_hist = [];
			for run in range(NRUNS):
				spikes = np.loadtxt( './data/single_%d_%d_%s_%d/spikesperpattern.dat'%(dend_cond, CLUSTERED, prp, run), dtype=float)
				spikes = spikes[ 0:NPYRS]
				tr=  trevrolls(spikes)
				trs[CLUSTERED, did, run] = tr;
				ff = np.mean(spikes);
				ffs[CLUSTERED, did, run] = ff/4.;
				pops[CLUSTERED, did, run] = 100.* sum(spikes>=40.) / float(NPYRS)

				syns = np.loadtxt('./data/single_%d_%d_%s_%d/syn-post.txt'%(dend_cond, CLUSTERED, prp, run), dtype=float)
				syns = syns[syns[:,4]>0.7]
				cols = ['input_id', 'group_id', 'branch_id','nid','weight']
				table = pd.DataFrame(syns,columns=cols)
				totals = table.groupby(['branch_id'])['weight'].count().values
				branch_hist.extend(totals.tolist())

				ratio_clustered[CLUSTERED, did, run] = sum(totals>2) / float(sum(totals>0))

			#plt.figure()
			#plt.title('Synapses per branch cond=%d'%(dend_cond));
			#df = pd.DataFrame(np.array(branch_hist), columns=['cnt'])
			#df['cnt'].value_counts().plot(kind='bar')
			#plt.ylim(ymin=0)
			#plt.xticks(np.arange(4), ['supra', 'sub', 'linear', 'mixed']);	




	plt.figure(figsize=(8,6))


	#trs = trs[2:3, :];

	#print( stats.f_oneway( trs[0,:] , trs[1,:] ) )

	#tr_means = np.mean(trs[0], 1)
	#tr_std =  np.std(trs[0],1)
	xr = np.arange(XLEN)
	ax = plt.subplot(2,2,1)
	plt.title('PRP %s'%(prp));

	plt.bar(xr-.2, np.mean(pops[0], 1), yerr=np.std(pops[0],1), width=.3 )
	plt.bar(xr+.2, np.mean(pops[1], 1), yerr=np.std(pops[1],1), width=.3 )

	print np.mean(pops[0], 1), np.std(pops[0],1) 
	print np.mean(pops[1], 1), np.std(pops[1],1) 


	plt.legend(['Dispersed', 'Clustered'])
	printpairstats(pops, 'Populations')

	plt.xticks(np.arange(XLEN), dend_ticks);
	plt.ylim(ymin=5)
	plt.ylabel('Engram Size (%) ');




	plt.subplot(2,2,2)

	#ffs = ffs[2:3,:];
	plt.bar(xr-.2, np.mean(ffs[0], 1), yerr=np.std(ffs[0],1), width=.3 )
	plt.bar(xr+.2, np.mean(ffs[1], 1), yerr=np.std(ffs[1],1), width=.3 )
	printpairstats(ffs, 'Firing')
	plt.xticks(np.arange(XLEN), dend_ticks);
	plt.ylim(ymin=5)
	plt.ylabel('Mean Firing Rate (Hz) ');


	plt.subplot(2,2,3)

	plt.bar(xr-.2, np.mean(trs[0], 1), yerr=np.std(trs[0],1), width=.3 )
	plt.bar(xr+.2, np.mean(trs[1], 1), yerr=np.std(trs[1],1), width=.3 )

	print np.mean(trs[0], 1), np.std(trs[0],1) 
	print np.mean(trs[1], 1), np.std(trs[1],1) 

	printpairstats(trs, 'Sparsity')
	#plt.ylim(ymin=0.4)
	plt.xticks(np.arange(XLEN), dend_ticks);
	plt.ylabel('T-R Sparsity');




	plt.subplot(2,2,4)

	ratio_clustered *= 100.
	plt.bar(xr-.2, np.mean(ratio_clustered[0], 1), yerr=np.std(ratio_clustered[0],1), width=.3 )
	plt.bar(xr+.2, np.mean(ratio_clustered[1], 1), yerr=np.std(ratio_clustered[1],1), width=.3 )
	printpairstats(ratio_clustered, 'Clustered')
	plt.xticks(np.arange(XLEN), dend_ticks);
	plt.ylim(ymin=10)
	plt.ylabel('Clustered Engram Synapses (%)');



	plt.savefig("clust_%s.pdf"%(prp))

plt.show();

