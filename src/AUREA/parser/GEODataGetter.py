import os, yaml, re
from warn import *
from GEO import GEO
from GEO.Sample import Sample
from GEO.Factory import Factory
from AUREA.parser.affyprobe2genesymbol import AffyProbe2GeneSymbol

class GEODataGetter(object):
    def __init__(self, name):
        self.name=name
        self.geo_ids=[]
        self.matrix=[]
        self.probe_index={}
        self.gene_index={}
        self.samples=[]
        self.sample_index={}
        self.af2gs=AffyProbe2GeneSymbol()
        self.preferred_id_type='gene'
        self.second_type='probe'
        self.subsets=[]

	# need to set:
	# self.dt_id
	# self.samples (list of sample names)
	# self.sample_descriptions (list of sample descriptions, each of which might be a list of lines)
	# self.genes (list of gene names)
	# self.probes (list of probe names)
	# self.matrix (2D data matrix: [gene/probe index][sample_index]
	# self.subsets (as necessary) (subsets set but not used by DataTable, others might access)

    def n_samples(self):
        return len(self.samples)

    def add_geo(self, geo):
        factory=Factory()

        s_ids=[]
        if factory.id2class(geo.geo_id) == Sample: s_ids=[geo.geo_id]
        else: s_ids=[geo.sample_ids]
            
        for sample_id in s_ids:
            sample=Sample(sample_id)
            self.add_sample(sample)

        self.add_entities(geo)

        
    def add_geo_id(self, geo_id):
        factory=Factory()
        geo=factory.newGEO(geo_id)
        self.add_geo(geo)


    ########################################################################
    def add_entities(self, geo):
        # 
            
        # add sample_descriptions: dict
        # add subsets
        # need formats...


    ########################################################################
    # Build self.table, self.gene_index, self.probe_index, self.sample_index

    def add_sample(self, sample, id_type='gene'): # sample is a GEO.Sample object
        # need to populate: new column to self.data_table, self.genes or self.probes, 
        # self.samples, self.gene_index or self.probe_index
        # and maybe more, like self.sample_description

        # ok, some sanity checking first: 
        if not isinstance(sample, Sample):
            raise Exception("%s: not a Sample object", sample)
        if not re.search('^gene|probe$', id_type):
            raise Exception('id_type must be one of "gene" or "probe"')
        if sample.geo_id in self.samples: # sample.geo_id is used as the sample name
            return                        # already added

        # add the sample name:
        self.samples.append(sample.geo_id)
        sample_i=self.n_samples()
        self.sample_index[sample.geo_id]=sample_i

        # get the data as a vector hash (pass on exceptions)
        try:    (id_type, sample_data)=sample.expression_data(id_type='gene')
        except: (id_type, sample_data)=sample.expression_data(id_type='probe')

        # add genes in sample to matrix, backfilling new genes, and converting types if necessary:
        for gene_id, exp_val in sample_data.items():
            if id_type == 'probe':
                probe_id=gene_id
                gene_id=self.probe2gene(gene_id)
            try:             gi=self.gene_index[gene_id]
            except KeyError: gi=self.add_gene(gene_id)
            row=self.matrix[gi]
            row.append(exp_val) # Is this slow?
        
        # for any genes in the table but not in the sample, set their value to 0
        for gene_id in self.genes():
            if gene_id not in sample_data:
                i=self.gene_index[gene_id]
                self.matrix[i].append(0.0)
        

        
    def probe2gene(self, probe_id):
        return self.af2gs.p2g(probe_id)

    def gene2probes(self, gene_id):
        return self.af2gs.g2ps(gene_id)


    ########################################################################
    # Backfill a gene:
    # - Set expression values in samples to 0
    # - Add gene id to self.gene_index, probe_id to probe_index
    # return new index
    def add_gene(self, gene_id):
        gene_index=self.gene_index
        i=len(gene_index)
        gene_index[gene_id]=i   # hash assignment, not array

        # add new row to self matrix:
        new_row=[0]*self.n_samples()
        self.matrix.append(new_row)
#        warn("add_gene(%s): matrix has %d rows, %d samples" % (gene_id, len(self.matrix), self.n_samples()))

        # add to self.probe_index, checking for conflicts
        for probe_id in self.gene2probes(gene_id):
            if probe_id in self.probe_index and self.probe_index[probe_id] != i: 
                raise Exception("duplicate probe_index for %s: old=%s, new=%s" % (gene_id, probe_id, self.probe_index[probe_id], i))
            self.probe_index[probe_id]=i
        return i


    def genes(self):
        return self.gene_index.keys()

    def probes(self):
        return self.probe_index.keys()




'''        
        # set the sample list and index:
        self.samples.append(sample.geo_id)
        self.sample_index[sample.geo_id]=len(self.samples)-1
        try: self.sample_description[geo_id]=sample.description
        except AttributeError: pass
        n_samples=len(self.samples)

        # get the proper (gene or probe) id_list and index to use:
        exp_data=sample.expression_data(id_type)
        ids=self.genes if id_type == 'gene' else self.probes
        if not ids: ids=[]
        index=self.gene_index if id_type == 'gene' else self.probe_index
        if not index: index={}

        # add any of sample's genes to self.genes as needed, and rebuild the index:
        #  fixme: have to back-fill missing genes for previous samples
        ids_added=False
        if not hasattr(self, 'data_table'): self.data_table=[]
        for key_id in exp_data.keys():
            if key_id not in index:
                ids.append(key_id)
                ids_added=True
                backfill_list=[0.0]*(n_samples-1)
                self.data_table.append(backfill_list)

        if id_type == 'gene': 
            self.genes=ids      # add additions back in
            if ids_added: self.buildGeneIndex()
            index=self.gene_index
            n_ids=len(self.genes)
        else: 
            self.probes=ids
            if ids_added: self.buildProbeIndex()
            index=self.probe_index
            n_ids=len(self.probes)

        # create a column of data according to gene_ or probe_index, and add to self:
        # self.data_table[index[gene]] [index[sample]]
#        if not hasattr(self, 'data_table'): self.data_table=[list(x) for x in [[]]*n_ids]

        for (gene_id, value) in sample.data[id_type].items(): # (gene_id might be a probe_id)
            try: i=index[gene_id]
            except KeyError: raise Exception("unknown gene- or probe_id %s" % gene_id)
            gene_list=self.data_table[i]
            gene_list.append(value)



'''
