import re

def SimData():
    with open('templates/TestData.txt', 'rt') as file:
        data = file.read()

    dataSplit = re.split(",+",data)

    t=[]
    p=[]
    i=0
    pattern = re.compile(r"\bt\w*\b")
    for line in dataSplit:
        if pattern.search(line) != None:
            t.append(line.strip(" t"))
            p.append(dataSplit[i+1].strip(" p"))
        i=i+1
    
    pattern = re.compile(r"\b\w*00000\b")
    tList = []
    pList = []
    i=0
    for line in t:
        if pattern.search(line) != None:
            tList.append(line)
            pList.append(p[i])
        i=i+1
    
    #sleepNum = 0.6
    #tSearch = str(sleepNum)
    #pattern = re.compile(r'({})00000'.format(tSearch))
    #pValue = []
    #i=0
    #for line in tList:
    #    if pattern.search(line) != None:
    #        pValue.append(pList[i])
    #    i=i+1  
    #pValuefl=float(pValue[0])
    print(tList)

    return tList, pList

if __name__=="__main__":
    SimData()