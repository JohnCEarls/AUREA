from AHREA.parser.CSVParser import CSVParser
from AHREA.packager.DataCleaner import DataTable
from AHREA.packager.DataPackager import dataPackager
csvFile = "data/testPackagerProbes1.csv"
p = CSVParser(csvFile,probe_column_name="probe", gene_column_name="probe")

print p.getColumnHeadings()
print p.getColumnHeadingsInfo()
#print p.getTable()
print p.getID_REF()
print p.getIDENTIFIER()
dt = DataTable(probe_column="probe", gene_column="probe")
dt.getCSVData(p)

dp = dataPackager()
dp.addDataTable(dt)
dp.writeToCSV("copyofacopy.csv")





