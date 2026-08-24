import os
import sys
myMIBNI_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'myMIBNI'))
sys.path.insert(0, myMIBNI_path)
import pandas as pd
from gene import GeneNetwork, Gene

class DataTimeSeries:
    '''
    Lớp đọc dữ liệu từ file để lấy các network
    '''
    def __init__(self, timeseries=None, goldstandard=None) -> None:
        self.timeseries = timeseries
        self.goldstandard = goldstandard
        self.size, self.networks = DataTimeSeries.read_timeseries(timeseries)
        self.samples = len(self.networks)
        self.goldstandard = DataTimeSeries.readGoldStandard(goldstandard)

        # print(self.goldstandard)
        # print(self.size)
        # print(self.networks)

    def networks_to_csv(self, folder=None, filename=None):
        '''
        convert all networks to csv file
        '''
        raw_csv = {}
        index=0
        for sample, genes in self.networks.items():
            for regulator, target, reaction in self.goldstandard:
                d = {'size': self.size, 'sample':sample, 'regulator':regulator, 'target':target, 'interaction': reaction}
                for i, v in enumerate(genes[regulator]):
                    d[f'r_step{i}'] = v
                for i, v in enumerate(genes[target]):
                    d[f't_step{i}'] = v
                raw_csv[index] = d
                index+=1
        data = pd.DataFrame.from_dict(raw_csv, orient='index')
        if folder is not None and filename is not None:
            data.to_csv(f'{folder}\{filename}.csv')
        return data 
        #result[f'st_0_{end}'] = {'precison': p, 'recall': r, 'structural': st, 'dynamics':dy}

    def getMultiNetworks(self):
        nets = []
        for index, net_infos in self.networks.items():
            nt = GeneNetwork()
            nodes = []
            for gene_name, values in net_infos.items():
                vals = [float(i) for i in values]
                nodes.append(Gene(gene_name, vals))
            nt.nodes = nodes
            nt.names = list(net_infos.keys())
            nt.timestepsNumber = len(nt.nodes[0].values)
            nt.timesteps = [i for i in range(nt.timestepsNumber)]
            nt.goldstandard = self.goldstandard
            nt.size = len(nt.nodes)
            nt.goldstandard_signed = None
            nt.dict_names = {f'{nt.names[i]}':f'G{i+1}' for i in range(nt.size)}
            nets.append(nt)
        return nets
            
    @staticmethod
    def read_timeseries(path):
        if path==None:
            return None
        f = open(path, "r")
        networks = {}
        networks_lines = {}
        genes_name = {}
        index=-1
        for x in f:
            if 'Time' in x:
                # lấy header
                headers = x[:-1].split('\t')[1:]
                #genes_name = {i:header[1:-1] for i, header in enumerate(headers)} #dream4
                genes_name = {i:header for i, header in enumerate(headers)}
            else:
                if x=='\n':
                    # dữ liệu của network
                    index+=1
                    networks_lines[index] = []
                else:
                    line = x[:-1].split('\t')[1:]
                    networks_lines[index].append(line)

        for k, v in networks_lines.items():
            #networks[k] = {gene[1:-1]:[] for gene in headers} #dream4
            networks[k] = {gene:[] for gene in headers}
            for timestep in v:
                for gene_index, value in enumerate(timestep):
                    networks[k][genes_name[gene_index]].append(value)
        return len(headers), networks
    
    @staticmethod
    def readGoldStandard(path):
        '''
        Read the goldstandard file
        Returns:
        List of tuple that contains a pair of (regulator and target)
        '''
        if path==None:
            return None
        goldstandard = []
        with open(path, "r") as f:
            for x in f:
                goldstandard.append(tuple(x[:-1].split('\t')))
        return goldstandard
            

# for i in range(1,5):
#     dt = DataTimeSeries(fr'C:\caocao\gnw-master\ANN\single_size\test\data for comparison\size70\Ecoli-70-{i}_dream4_timeseries.tsv', 
#                         fr'C:\caocao\gnw-master\ANN\single_size\test\size70\Ecoli-70-{i}_goldstandard.tsv')
#     dt.networks_to_csv(r'C:\caocao\gnw-master\ANN\single_size\test\data for comparison\size70', f'size70_{i}')

# Dream4
# dt = DataTimeSeries(r'C:\caocao\gnw-master\DREAM4 in-silico challenge\Size 100\DREAM4 training data\insilico_size100_1\insilico_size100_1_timeseries.tsv', 
#                     r'C:\caocao\gnw-master\DREAM4 in-silico challenge\Size 100\DREAM4 gold standards\insilico_size100_1_goldstandard.tsv')
# dt.networks_to_csv(r'C:\caocao\gnw-master\DREAM4 in-silico challenge\ANN', 'size100_1')