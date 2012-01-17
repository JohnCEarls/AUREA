
from AUREA.learner import ktsp, tst, dirac, tsp
from AUREA.parser import SOFTParser, GMTParser, SettingsParser, CSVParser
from AUREA.packager import DataCleaner, DataPackager
from AUREA.heuristic import ResourceEstimate, LearnerQueue
import os
def runAUREA(in1, in2, learner, config):
    #check inputs
    resultString = ""
    if not os.path.isfile(str(in1)):
        resultString += "ERROR: input table 1["+ str(in1)  + "] does not exist\n"
    if not os.path.isfile(str(in2)):
        resultString += "ERROR: input table 2["+ str(in2)  + "] does not exist\n"
    if not os.path.isfile(str(config)):
        resultString += "ERROR: config file ["+ str(config)  + "] does not exist\n"
    valid_learners =  ['tsp', 'tst', 'ktsp', 'dirac', 'adaptive']
    if learner not in valid_learners:
        resultString +=  "ERROR: " + str(learner) + " is not a valid learner.\n"
        resultString +=  "\tvalid options are [" + " ".join(valid_learners) + "]\n"
    if len(resultString) > 0:
        return resultString

    dp = buildData(in1, in2)
    data_vector, num_genes = dp.getDataVector('probe')
    print num_genes
    print len(data_vector)


def buildData(file1, file2):
    gnfile  = "c2.biocarta.v2.5.symbols.gmt"
    synfile = "Homo_sapiens.gene_info.gz"
    gnf = GMTParser.GMTParser(gnfile)
    f1 = CSVParser.CSVParser(file1, probe_column_name="probe", gene_column_name="gene")
    f2 = CSVParser.CSVParser(file2, probe_column_name="probe", gene_column_name="gene")
    dt1 = DataCleaner.DataTable(probe_column="probe", gene_column="gene")
    dt1.getCSVData(f1)
    dt2 = DataCleaner.DataTable(probe_column="probe", gene_column="gene")
    dt2.getCSVData(f2)

    dp = DataPackager.dataPackager(merge_cache=".")
    dp.addDataTable(dt1)
    dp.addDataTable(dt2)
    dp.createClassification("f1")
    for samp in f1.getDataColumnHeadings():
        dp.addToClassification("f1", dt1.dt_id, samp)
    dp.createClassification("f2")
    for samp in f2.getDataColumnHeadings():
        dp.addToClassification("f2", dt2.dt_id, samp)
    return dp




if __name__ == "__main__":
    from optparse import OptionParser
    
    parser = OptionParser()
    parser.add_option("-a", "--table_1", dest="input_file_one",
                        help="csv file for class 1")
    parser.add_option("-b", "--table_2", dest="input_file_two",
                        help="csv file for class 2")
    parser.add_option("-l", "--learner", dest="learner",
                        help="learner to train (tsp, tst, ktsp, dirac, adaptive)")
    parser.add_option("-c", "--config", dest="config_file",
                        help="xml file containing the learner settings")
    parser.add_option("-o", "--output", dest="output_file",
                        help="file in which to write output(defaults to std out)")
    

    (options, args) = parser.parse_args()
    
    if options.output_file is None:
        print runAUREA(options.input_file_one, options.input_file_two, options.learner, options.config_file)

    print options.input_file_one
    print options.input_file_two


    

