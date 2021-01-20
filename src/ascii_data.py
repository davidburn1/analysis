import numpy as np

def loadI10Data(filename):
 
    headerIndex = 0
    processMetadata = 0
    metadata = {}
    
    
    f = open(filename, "r") 
    line = 1
    while line:
        line = f.readline()
        
        # process metadata 
        if (line == "</MetaDataAtStart>\n"):
            processMetadata = 0
        if (processMetadata == 1):
            md = line[:-1].split("=")
            metadata[md[0]] = md[1]
        if (line == "<MetaDataAtStart>\n"):
            processMetadata = 1
        
        #find end of header
        if (line == " &END\n"):
            headings = f.readline()
            headings = headings[:-1].split("\t")
            headerIndex = headerIndex + 2
            break
  
        headerIndex = headerIndex +1
    f.close()
    
    data = np.genfromtxt(filename,delimiter='\t',skip_header=headerIndex)
    data = np.transpose(data)

    
    out = {}
    out['metadata'] = metadata
    for i, heading in enumerate(headings):
        out[heading] = data[i]

    return out
