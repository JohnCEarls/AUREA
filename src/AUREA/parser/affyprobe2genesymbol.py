from Mongoid import Mongoid
from warn import *

class AffyProbe2GeneSymbol(Mongoid):
    db_name='babel'
    collection_name='affyProbe2geneSym'

    def p2g(self, probe_id):
        ''' translate a probe_id to a gene symbol '''
        '''
        query={'affy_probe':probe_id}
        warn("looking for %s in %s" % (query, self.mongo().name))
        record=self.mongo().find_one(query)
        warn("found %s" % record)
        '''
        return self.mongo().find_one({'affy_probe':probe_id})['gene_symbol']
        
    def g2ps(self, gene_id):
        return [x['affy_probe'] for x in list(self.mongo().find({"gene_symbol":gene_id}))]
