import os
import glob

def raw2sample_idDicMaker(mycellistfile):
    idDic = dict()
    for line in open(mycellistfile):
        items = line.strip().split()
        idDic.setdefault(items[0], items[1])
    return idDic

def cel(mycellistfile, linkedCelDir, targetDir):
    if not os.path.isdir(targetDir):
        os.mkdir(targetDir)
    idDic = raw2sample_idDicMaker(mycellistfile)
    for aCelFile in glob.glob('{0}/*.CEL'.format(linkedCelDir)):
        cel_name = aCelFile.split('/')[-1].split('.')[0]
        sample_name = idDic[cel_name]
        symFile = '{0}/{1}.CEL'.format(targetDir, sample_name)
        try:
            #print '#SYMLINK : {0} -> {1}'.format(aCelFile, symFile)
            os.symlink(aCelFile, symFile)
        except OSError as e:
            os.unlink(symFile)
            os.symlink(aCelFile, symFile)

def aFileSymlinker(aFile, lnName, targetDir):
    print '#UPLOADER : {0}'.format(aFile)
    if not os.path.isdir(targetDir):
        os.mkdir(targetDir)
    targetFile = '{0}/{1}'.format(targetDir, lnName)
    try:
        os.symlink(aFile, targetFile)
    except OSError as e:
        os.unlink(targetFile)
        os.symlink(aFile, targetFile)

def main():
    pass

if __name__=='__main__':
    main()
