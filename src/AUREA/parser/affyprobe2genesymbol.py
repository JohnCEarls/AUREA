from Mongoid import Mongoid

class AffyProbe2GeneSymbol(Mongoid):
    db_name='babel'
    collection_name='affyProbe2geneSym'

    def p2g(self, probe_id):
        return self.mongo().find_one({'affy_probe':probe_id})['gene_symbol']
        
    def g2ps(self, gene_id):
        return [x['affy_probe'] for x in list(self.mongo().find({"gene_symbol":gene_id}))]
