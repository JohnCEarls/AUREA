from Mongoid import Mongoid
from warn import *

class AffyProbe2GeneSymbol(Mongoid):
    db_name='babel'
    collection_name='affyProbe2geneSym'

    def p2g(self, probe_id):
        ''' translate a probe_id to a gene symbol '''
        ''' retain this for debugging purposes
        query={'affy_probe':probe_id}
        warn("looking for %s in %s" % (query, self.mongo().name))
        record=self.mongo().find_one(query)
        warn("found %s" % record)
        '''
        try: return self.mongo().find_one({'affy_probe':probe_id})['gene_symbol']
        except TypeError as e: raise Exception('no gene symbol for %s' % probe_id)
        except KeyError as e: raise Exception('no gene symbol for %s (%s)' % (probe_id, type(e)))
        
    def g2ps(self, gene_id):
        return [x['affy_probe'] for x in list(self.mongo().find({"gene_symbol":gene_id}))]

    def all(self):
        ''' return a dict containing all the probe->gene translations '''
        warn("AffyProbe2GeneSymbol: creating local dictionaries...\n")
        cur=self.mongo().find()
        p2g=dict()
        g2p=dict()
        while(True):
            try: pair=cur.next()
            except: break
            probe_id=pair['affy_probe']
            symbol=pair['gene_symbol']
            p2g[probe_id]=symbol
            if symbol not in g2p: g2p[symbol]=[]
            g2p[symbol].append(probe_id)
        return (p2g,g2p)


