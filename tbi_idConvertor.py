import os

def idDicMaker(idConvertedFile):
    idDic = dict()
    for line in open(idConvertedFile):
        items = line.strip().split()
        idDic.setdefault(items[1], items[2])
    return idDic

def cel_col(infile, prjt_id, delimiter, col_idx, idConvertedFile):
    print '#ID_CONVERTOR : {0}'.format(infile)
    idDic = idDicMaker(idConvertedFile)

    fName, ext = os.path.splitext(infile)
    outfile = '{0}.{1}{2}'.format(fName, prjt_id, ext)
    out = open(outfile, 'w')
    for line in open(infile):
        items = line.strip().split(delimiter)
        if items[int(col_idx)] in idDic:
            items[int(col_idx)] = idDic[items[int(col_idx)]]
        out.write('{0}\n'.format(delimiter.join(items)))
    out.close()

    return outfile

def cel_title(infile, prjt_id, delimiter, startText, idConvertedFile):
    print '#ID_CONVERTOR : {0}'.format(infile)
    idDic = idDicMaker(idConvertedFile)

    fName, ext = os.path.splitext(infile)
    outfile = '{0}.{1}{2}'.format(fName, prjt_id, ext)
    out = open(outfile, 'w')
    for line in open(infile):
        items = line.strip().split(delimiter)
        if line.startswith(startText):
            for idx, item in enumerate(items):
                if len(item.split('.CEL')) in [1]:
                    key = '{0}.CEL'.format(item.split('.CEL')[0])
                else:
                    key = '{0}.CEL'.format(item.split('.CEL')[0])
                    residue = '{0}'.format(item.split('.CEL')[1])
                if key in idDic:
                    if len(item.split('.CEL')) in [1]:
                        items[idx] = '{0}.CEL'.format(idDic[key])
                    else:
                        items[idx] = '{0}.CEL{1}'.format(idDic[key], residue)
        out.write('{0}\n'.format(delimiter.join(items)))
    out.close()

    return outfile

def idDicMaker_anno(annoCsvFile, annoIdx):
    import csv
    idDic = dict()
    with open(annoCsvFile) as csvFile:
        for items in csv.reader(csvFile):
            if items[0].startswith('#'):
                continue
            idDic.setdefault(items[0], items[annoIdx])
    return idDic

def snpId_col(infile, prjt_id, delimiter, col_idx, annoCsvFile, annoIdx):
    print '#ID_CONVERTOR : {0}'.format(infile)
    idDic = idDicMaker_anno(annoCsvFile, annoIdx)

    fName, ext = os.path.splitext(infile)
    outfile = '{0}.{1}{2}'.format(fName, prjt_id, ext)
    out = open(outfile, 'w')
    for line in open(infile):
        items = line.strip().split(delimiter)
        if line.startswith('#'):
            out.write(line)
            continue
        if items[col_idx] in idDic:
            if not idDic[items[col_idx]] in ['---']:
                items[col_idx] = idDic[items[col_idx]]
        out.write('{0}\n'.format(delimiter.join(items)))
    out.close()

    return outfile


def row():
    pass

def main():
    pass

if __name__=='__main__':
    main()
