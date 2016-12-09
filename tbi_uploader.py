import os
import glob

def raw2sample_idDicMaker(idConvertedFile):
    idDic = dict()
    for line in open(idConvertedFile):
        items = line.strip().split()
        idDic.setdefault(items[1].split('.CEL')[0], items[2])
    return idDic

def cel(idConvertedFile, linkedCelDir, targetDir):
    if not os.path.isdir(targetDir):
        os.makedirs(targetDir)
    idDic = raw2sample_idDicMaker(idConvertedFile)
    for aCelFile in glob.glob('{0}/*.CEL'.format(linkedCelDir)):
        cel_name = aCelFile.split('/')[-1].split('.CEL')[0]
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
