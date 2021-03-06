//
// Version: $Id: lamodel.cpp 172 2014-02-12 10:06:07Z gk $
//

/* 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


#include "constructs.h"
#include <iostream>
#include <cstring>
#include <string>
#include <unistd.h>
#include <getopt.h>



int main( int argc, char* argv[])
{
	
	int c;


	// Set defaults
	int nneurons = 500;
	int nbranches = 20;
	int ninputs = 400;
	int nperinput = 1;
	int npatterns = ninputs;
	int nonesperpattern = 1;
	int interstim = 60;
	int rseed = 1980;
	char* suffix = NULL;
	bool storeData = false;
	bool disableCreb = false;
	int patternsOverlapping = -1;

	LANetwork net; 
	net.enablePruning = false; // default

	while ((c = getopt(argc, argv, "M:N:H:B:I:i:P:p:T:S:s:d:w:O:g:l:h:b:c:o:t:xnLDRJCGU"))!= -1)
	{
		switch (c)
		{
			case '?':
			cout << "usage: "<< argv[0] << " -N nneurons -B nbranches   -P npatterns -p ones_per_pattern -d overlappingPatternOffset -T interstim -S random_seed -w weakMemId " << endl;
			return 1;
			break;

			case 'B': nbranches = atoi(optarg); break;
			//case 'I': ninputs = atoi(optarg); break;
			//case 'i': nperinput = atoi(optarg); break;
			case 'N': nneurons = atoi(optarg); break;
			case 'P': npatterns = atoi(optarg); break;
			case 'p': nonesperpattern = atoi(optarg); break;
			case 'T': interstim = atoi(optarg); break;
			case 'S': rseed = ( atoi(optarg)); break;
			case 's': suffix = strdup(optarg); break;
			case 'd': patternsOverlapping = atoi(optarg); break;

			case 'x': storeData = true; break;
			case 'n': disableCreb = true; break;
			case 'w': net.isWeakMem.push_back(atoi(optarg)-1); break;

			case 'L': net.localProteins = true; break;
			case 'G': net.globalProteins = true; break;
			case 'D': net.debugMode = true; break;
			case 'R': net.repeatedLearning = true; break;
			case 'J': net.pretraining = true; break;
			case 'C': net.altConnectivity = true; break;
			case 'O': net.branchOverlap = atof(optarg); break;
			case 'H': net.homeostasisTime = atof(optarg); break;


			case 'o': 
				char* o = strstr(optarg, "=");
				if (o)
				{
					*o = '\0';
					char* val = o+1;

					if (!strcmp(optarg, "connectivityParam")) net.connectivityParam = atof(val); 
					else if (!strcmp(optarg,  "BSPTimeParam")) net.BSPTimeParam = atof(val); 
					else if (!strcmp(optarg,  "homeostasisTimeParam")) net.homeostasisTimeParam = atof(val); 
					else if (!strcmp(optarg,  "CREBTimeParam")) net.CREBTimeParam = atof(val); 
					else if (!strcmp(optarg,  "inhibitionParam")) net.inhibitionParam = atof(val); 

					else if (!strcmp(optarg,  "globalPRPThresh")) net.globalPRPThresh = atof(val); 
					else if (!strcmp(optarg,  "localPRPThresh")) net.localPRPThresh = atof(val); 
					else if (!strcmp(optarg,  "dendSpikeThresh")) net.dendSpikeThresh = atof(val); 

					else if (!strcmp(optarg,  "initWeight")) net.initWeight*= atof(val); 
					else if (!strcmp(optarg,  "maxWeight")) net.maxWeight*= atof(val); 
					else if (!strcmp(optarg,  "stimDurationParam")) net.stimDurationParam = atof(val); 
					else if (!strcmp(optarg,  "nNeuronsParam")) nneurons *= atof(val); 
					else if (!strcmp(optarg,  "nBranchesParam")) nbranches *= atof(val); 
					else if (!strcmp(optarg,  "nBranchesTurnover")) net.nBranchesTurnover = atoi(val); 
					else if (!strcmp(optarg,  "INClustered")) net.INClustered = atoi(val); 
					else if (!strcmp(optarg,  "setNlTypes")) net.setNlTypes = atoi(val); 
					else if (!strcmp(optarg,  "enableTurnover")) net.enableTurnover = atoi(val); 

					else if (!strcmp(optarg,  "inSomaTau"))  net.inSomaTau  = atof(val);
					else if (!strcmp(optarg,  "pyrSomaTau")) net.pyrSomaTau = atof(val);

					else if (!strcmp(optarg,  "inDendrites")) net.inDendrites = atoi(val);
					else { 
						printf("[Error] Invalid option '%s'\n", optarg);
						exit(1);
					}

					printf("[Option] '%s' value='%s'\n", optarg, val);
				}
			break;
		}
	}


	LANetwork::SetRandomSeed(rseed);
	net.disableCreb = disableCreb;

	// Override;
	ninputs = nonesperpattern * npatterns;
	printf("\nInputs=%d, neurons per input=%d, memories to encode=%d\n", ninputs, nperinput, npatterns);
	net.CreateFearNet(nneurons, nbranches, ninputs, nperinput);

	char buf[512];
	if (suffix)
		sprintf(buf, "./data/%s", suffix );
	else
		sprintf(buf, "./data/N%d.B%d.I%d.i%d.P%d.p%d.T%d.S%d.w%d_%s", nneurons, nbranches, ninputs, nperinput, npatterns, nonesperpattern, interstim, rseed, (int)net.isWeakMem.size(),  suffix ? suffix : "");
	cout << "Output data dir: "<< buf <<  endl;

	net.SetDataDir( buf);

	if (net.pretraining)
	{
		char buf2[1024];
		sprintf(buf2, "%s/%s", buf, "pre-syn.dat");
		net.SaveSynapseState(buf2);
	}

	net.RunStoreTest(npatterns, nonesperpattern, interstim, 0, patternsOverlapping);
	cout << "Storing data files ..."<< endl;
	cout<<buf << endl;
	net.StoreDataFiles( storeData);
	printf("Done!\n");

	char buf2[512];
	sprintf(buf2, "cp constructs.cpp %s/", buf);
	system(buf2);

	return 0;
}



