import os, yaml, re
from warn import *
import GEO

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
        self.sample_descriptions={}
        self.sample_index={}
        self.af2gs=AffyProbe2GeneSymbol()
        (self.p2g, self.g2p)=self.af2gs.all()
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

    def add_geo(self, geo, id_type='probe'):
        factory=Factory()

        s_ids=[]
        cls=factory.id2class(geo.geo_id)
        if cls == GEO.Sample.Sample: s_ids=[geo.geo_id]
        else: 
            try: s_ids=geo.sample_id
            except AttributeError:
                raise Exception("no samples for %s" % geo.geo_id)
            
        for sample_id in s_ids:
            sample=Sample(sample_id)
            self.add_sample(sample, id_type)

        self.add_entities(geo)

        
    def add_geo_id(self, geo_id, id_type='probe'):
        factory=Factory()
        geo=factory.newGEO(geo_id).populate()
#        warn("geo is %s" % yaml.dump(geo))
        self.add_geo(geo, id_type)


    ########################################################################
    def add_entities(self, geo):
        pass

        # 
            
        # add sample_descriptions: dict
        # add subsets
        # need formats...


    ########################################################################
    # Build self.table, self.gene_index, self.probe_index, self.sample_index
    # return number of genes for which no expression value can be assigned

    def add_sample(self, sample, id_type='gene'): # sample is a GEO.Sample object
        # need to populate: new column to self.data_table, self.genes or self.probes, 
        # self.samples, self.gene_index or self.probe_index
        # and maybe more, like self.sample_description
        warn("adding %s (%s)" % (sample.geo_id, id_type))

        # ok, some sanity checking first: 
        if not isinstance(sample, Sample):
            raise Exception("%s: not a Sample object", sample)
        if not re.search('^gene|probe$', id_type):
            raise Exception('id_type must be one of "gene" or "probe"')
        if sample.geo_id in self.samples: # sample.geo_id is used as the sample name
            return                        # already added

        # add the sample name, description, index:
        self.samples.append(sample.geo_id)
        sample_i=self.n_samples()
        self.sample_index[sample.geo_id]=sample_i
        try: self.sample_descriptions[sample.geo_id]=sample.description
        except AttributeError: 
#            warn("no sample.description for %s" % sample.geo_id)
#            warn("other descriptions: %s" % sample.descriptions())
            pass

        # get the data as a vector hash (pass on exceptions)
        try:    (id_type, sample_data)=sample.expression_data(id_type='gene')
        except: (id_type, sample_data)=sample.expression_data(id_type='probe')
        if id_type=='gene': index=self.gene_index
        else:               index=self.probe_index
            
        # add genes in sample to matrix, backfilling new genes, and converting types if necessary:
        for gene_id, exp_val in sample_data.items():
            if id_type == 'probe': # ...unless it's not
                probe_id=gene_id 
                try: gene_id=self.p2g[gene_id] # look up the gene_id
                except: pass    # leave gene_id and probe_id the same
            else:
                probe_id=self.g2p[gene_id]
            warn("gene_id=%s, probe_id=%s" % (gene_id, probe_id))

            # get row index (i_row):
#            try: i_row=index[gene_id]
            try: i_row=self.gene_index[gene_id]
            except KeyError:    # first time for gene_id
                try: probe_ids=self.g2p[gene_id]
                except KeyError: probe_ids=[]
                warn("%s (%s): no index for %s (%s)" %(sample.geo_id, id_type, gene_id, ','.join(probe_ids)))
                i_row=self.add_gene(gene_id, probe_id)
                
            row=self.matrix[i_row]
            row.append(exp_val) # Is this slow?

        # for any genes in the table but not in the sample, set their value to 0
        # what about probe ids not here?  Since we're appending, we could check 
        # len(matrix[i]), take too long?
        for gene_id in self.genes():
            if gene_id not in sample_data:
                i=self.gene_index[gene_id]
                self.matrix[i].append(0.0)
                warn("setting %s %s[%i] to zero" % (sample.geo_id, gene_id, i))
        


        
    def probe2gene(self, probe_id):
        return self.af2gs.p2g(probe_id)

    def gene2probes(self, gene_id):
        return self.af2gs.g2ps(gene_id)


    ########################################################################
    # Backfill a gene:
    # - Set expression values in samples to 0
    # - Add gene id to self.gene_index, probe_id to probe_index
    # Note: It's possibe that gene_id is really a probe_id for an unmapped gene
    # return new index
    def add_gene(self, gene_id, probe_id):
        gene_index=self.gene_index
        i=len(gene_index)
        gene_index[gene_id]=i   # hash assignment, not array
        warn("add_gene: gene_index[%s]=%i" % (gene_id, i))

        # add new row to self matrix:
        new_row=[0]*self.n_samples()
        self.matrix.append(new_row)
#        warn("add_gene(%s): matrix has %d rows, %d samples" % (gene_id, len(self.matrix), self.n_samples()))

        # add to self.probe_index, checking for conflicts
        if probe_id != gene_id:
            try: probe_ids=self.g2p[gene_id]
            except KeyError: probe_ids=[gene_id] # happens when probe_id has no mapping
        else:
            probe_ids=[probe_id]

        for probe_id in probe_ids:
            if probe_id in self.probe_index and self.probe_index[probe_id] != i: 
                raise Exception("duplicate probe_index for %s(%s): old g_index=%d, new index=%d" % (gene_id, probe_id, self.probe_index[probe_id], i))
            self.probe_index[probe_id]=i

        warn("gene added: g=%s[%d], ps=%s[%s], " %(gene_id, gene_index[gene_id], 
                                                   ",".join(probe_ids),
                                                   ",".join([str(self.probe_index[x]) for x in probe_ids])
                                                   ))
        return i


    def genes(self):
        return self.gene_index.keys()

    def n_genes(self):
        return len(self.genes())

    def probes(self):
        return self.probe_index.keys()

    def n_probes(self):
        return len(self.probes())

    def n_samples(self):
        return len(self.samples)


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
        
