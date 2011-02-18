from tfidf import *
import psycopg2
import psycopg2.extensions
import math
def cos_sim(A,B):
    def dot_product(a,b):
        sum = 0.0
        for key in a.keys():
            if key in b:
                sum += a[key]*b[key]
        return sum
    return dot_product(A,B)/(math.sqrt(dot_product(A,A)) * math.sqrt(dot_product(B,B)))

conn = psycopg2.connect("host=localhost dbname=SOFTFile user=AHREA password=AHREA")
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
c = conn.cursor()
qry = "SELECT dataset_id, dataset_title, dataset_description \
        FROM dataset"

#WHERE dataset_id < 20"
c.execute(qry)
documentList = []
documentNumber = 0
docMap = []
for id,title, description in c.fetchall():
    documentList.append(title + description)
    docMap.append(id)
c.close()
vectors = []
print "gotDocs"
for x in range(len(documentList)):
    words = {}
    for word in documentList[documentNumber].split(None):
        words[word] = tfidf(word,documentList[documentNumber],documentList)

    #for item in sorted(words.items(), key=itemgetter(1), reverse=True):
    #    print "%f <= %s" % (item[1], item[0])
    vectors.append(words)
    documentNumber = x+1
print "got vectors"
sim = []
for i in range(len(vectors[:-1])):
    for j in range(i+1, len(vectors)):
        sim = cos_sim(vectors[i], vectors[j])
        db_id1 = docMap[i]
        db_id2 = docMap[j]
        qry = "INSERT into cosine_similarity(id1, id2, score) VALUES (%s, %s, %s)"
        c = conn.cursor()
        c.execute(qry, (db_id1, db_id2, sim))
        c.close()
