import os, yaml, re
from warn import *
import GEO

from GEO.Sample import Sample
from GEO.Factory import Factory

from AUREA.parser.affyprobe2genesymbol import AffyProbe2GeneSymbol

class GEODataGetter(object):
    def __init__(self, name):
        self.name=name
        self.af2gs=AffyProbe2GeneSymbol()
        self.p2g=None
        self.g2p=None
        self.clear()

	# need to set:
	# self.dt_id
	# self.samples (list of sample names)
	# self.sample_descriptions (list of sample descriptions, each of which might be a list of lines)
	# self.genes (list of gene names)
	# self.probes (list of probe names)
	# self.matrix (2D data matrix: [gene/probe index][sample_index]
	# self.subsets (as necessary) (subsets set but not used by DataTable, others might access)

    def clear(self):
        self.matrix=[]
        self.probe_index={}
        self.gene_index={}
        self.samples=[]
        self.sample_descriptions={}
        self.sample_index={}
        self.n_samples=0
        self.samples_added=0

        self.use_mask=False     # If these two hold values then only use the genes/probes listed
        self.mask={}            # 


    def genes(self):
        return self.gene_index.keys()

    def n_genes(self):
        return len(self.genes())

    def probes(self):
        return self.probe_index.keys()

    def n_probes(self):
        return len(self.probes())

    def has_sample(self, sample_id):
        return sample_id in self.sample_index

    ########################################################################

    def add_geo(self, geo):
        factory=Factory()
        cls=factory.id2class(geo.geo_id)

        s_ids=[]
        if cls == GEO.Sample.Sample: s_ids=[geo.geo_id]
        else: 
            try: s_ids=geo.sample_id
            except AttributeError:
                raise Exception("no samples for %s" % geo.geo_id)
            
        self.add_cols(len(s_ids))
        for sample_id in s_ids:
            sample=Sample(sample_id)
            self.add_sample(sample)

#        self.add_entities(geo)

        
    def add_geo_id(self, geo_id):
        geo=Factory().newGEO(geo_id).populate()
        self.add_geo(geo)
    

    ########################################################################
    # Build self.table, self.gene_index, self.probe_index, self.sample_index
    # return number of genes for which no expression value can be assigned

    def add_cols(self, n_cols):
        for row in self.matrix:
            row.extend([0] * n_cols)
        self.samples.extend([''] * n_cols)
        self.n_samples+=n_cols

    def add_sample(self, sample): # sample is a GEO.Sample object
        warn("adding %s" % sample.geo_id)

        # ok, some sanity checking first: 
        if not isinstance(sample, Sample):
            raise Exception("%s: not a Sample object", sample)
        if sample.geo_id in self.samples: # sample.geo_id is used as the sample name
            return                        # already added

        # add the sample name, description, index:
        i_sample=self.samples_added 
        self.samples_added+=1
        self.samples[i_sample]=sample.geo_id

        self.sample_index[sample.geo_id]=i_sample
        try: self.sample_descriptions[sample.geo_id]=sample.description
        except AttributeError: pass

        # add genes in sample to matrix, backfilling new genes, and converting types if necessary:
        (id_type, sample_data)=sample.expression_data(id_type='probe') # id_type unused
        for probe_id, exp_val in sample_data.items():
            if self.use_mask and probe_id not in self.mask: continue

            try: i_row=self.probe_index[probe_id]
            except KeyError: i_row=self.add_gene(probe_id)
            row=self.matrix[i_row]
            try:
                if row[i_sample] != 0:
                    warn("overwriting matrix[%s][%s] with %f -> %f" %(probe_id, sample.geo_id, row[i_sample], exp_val))
            except IndexError:
                raise Exception("tried to access row[%d], len(row)=%d, probe_id=%s, i_row=%d" % (i_sample, len(row), probe_id, i_row))
            row[i_sample]=exp_val

    def probe2gene(self, probe_id):
        if not self.p2g:
            (self.p2g, self.g2p)=self.af2gs.all()
        return self.af2gs.p2g(probe_id)

    def gene2probes(self, gene_id):
        if not self.g2p:
            (self.p2g, self.g2p)=self.af2gs.all()
        return self.af2gs.g2ps(gene_id)


    ########################################################################
    # Backfill a gene:
    # - Set expression values in samples to 0
    # - Add gene id to self.gene_index, probe_id to probe_index
    # Note: It's possibe that gene_id is really a probe_id for an unmapped gene
    # return new index
    def add_gene(self, probe_id):
        if probe_id in self.probe_index:
            raise Exception("duplicate probe_id %s" %(probe_id))
        i=len(self.probe_index)

        # add new row to self matrix:
        new_row=[0]*self.n_samples
        self.matrix.append(new_row)
        self.probe_index[probe_id]=i

        return i


    ########################################################################

    def writeCSV(self, filename):
        f=open(filename, 'w')

        # write header (sample names in order)
        f.write(",".join(self.samples)+"\n")
        
        # write each row:
        for i in range(self.n_genes()):
            gene_id=self.genes()[i]
            probe_ids=' '.join(self.g2p[gene_id])
            ids=','.join([gene_id, probe_ids])
            i_row=self.gene_index[gene_id]
            exp_vals=','.join(str(x) for x in self.matrix[i_row])
            f.write(','.join([ids, exp_vals])+"\n")

        f.close()
        warn("%s written" % filename)

    def write_gene_index(self, filename, mode='w'):
        f=open(filename, mode)
        for g in self.genes():
            f.write("\t".join([g, str(self.gene_index[g])])+"\n")
        
    def write_probe_index(self, filename, mode='w'):
        f=open(filename, mode)
        for g in self.probes():
            f.write("\t".join([g, str(self.probe_index[g])])+"\n")
        
    def write_sample_index(self, filename, mode='w'):
        f=open(filename, mode)
        for g in self.samples:
            f.write("\t".join([g, str(self.sample_index[g])])+"\n")
        
