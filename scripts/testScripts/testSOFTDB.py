from parser.SOFTParser import entity, SOFTParser

if __name__ == "__main__":
    import os
    for file in os.listdir("downloaded"):
        if file[-8:] == '.soft.gz':
            sp = SOFTParser("downloaded/"+file)
            sp.addEntitiesToDatabase()
