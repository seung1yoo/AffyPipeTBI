def targetCelSelector(targetCelFile, fh_log):
    celDic = dict()
    for line in open(targetCelFile):
        celFile = line.strip()
        celFile_re = celFile_Renaming(celFile)
        print >> fh_log, '#TARGET_CEL_RENAMING : {0} ---> {1}'\
                ''.format(celFile, celFile_re)
        celDic.setdefault(celFile_re, celFile)
    return celDic

def celFile_Renaming(celFile):
    nonextend_Filename = celFile.rstrip('.CEL')
    barcode = nonextend_Filename.split('_')[0]
    well_position = nonextend_Filename.split('_')[-1]
    celFile_re = '{0}_{1}.CEL'.format(barcode, well_position)
    return celFile_re

def celFileFinder(rawCelDir, fh_log):
    cmd = ['find', rawCelDir, '-iname', '*.CEL']
    fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    cel_files = fd_popen.read().strip()
    fd_popen.close()
    rawCelDic = dict()
    for cel_file in cel_files.split('\n'):
        cel_file_name = cel_file.split('/')[-1]
        celFile_re = celFile_Renaming(cel_file_name)
        print >> fh_log, '#RAW_CEL_RENAMING : {0} ---> {1}'\
                ''.format(cel_file, celFile_re)
        rawCelDic.setdefault(celFile_re,
                os.path.abspath(cel_file))
    return rawCelDic

def symbolicLinking(targetCelDic, rawCelDic, linkedCelDir):
    if not os.path.isdir(linkedCelDir):
        os.mkdir(linkedCelDir)

    cmdDic = dict()
    for t_celFile, t_celFile_ori in targetCelDic.iteritems():
        if t_celFile in rawCelDic:
            cmdDic.setdefault('cmd', {}).setdefault(t_celFile, [rawCelDic[t_celFile],
                    '{0}/{1}'.format(linkedCelDir, t_celFile)])
        else:
            cmdDic.setdefault('error', {}).setdefault(t_celFile,
                    '{0} target cel file is not in rawCelDir'.format(t_celFile))

    for tag, celFileDic in cmdDic.iteritems():
        for celFile, cmd in celFileDic.iteritems():
            if tag in ['cmd']:
                try:
                    os.symlink(cmd[0], cmd[1])
                except OSError:
                    os.unlink(cmd[1])
                    os.symlink(cmd[0], cmd[1])
            elif tag in ['error']:
                print celFile, cmd

    return cmdDic

def createcelfile_sh(cmdDic, linkedCelDir):
    out = open('{0}/mycellistfile.txt'.format(linkedCelDir), 'w')
    out.write('cel_files\n')
    for tag, celFileDic in cmdDic.iteritems():
        for celFile, cmd in celFileDic.iteritems():
            if tag in ['cmd']:
                out.write('{0}\n'.format(os.path.abspath(cmd[1])))
    out.close()

def main(args):
    fh_log = open(args.logFile, 'w')

    targetCelDic = targetCelSelector(args.targetCelFile, fh_log)
    print >> fh_log, '#MESSAGE {0} : Target CEL file count : {1}'\
            ''.format(datetime.today(), len(targetCelDic))

    rawCelDic = celFileFinder(args.rawCelDir, fh_log)
    print >> fh_log, '#MESSAGE {0} : Raw CEL file count : {1}'\
            ''.format(datetime.today(), len(rawCelDic))

    cmdDic = symbolicLinking(targetCelDic, rawCelDic, args.linkedCelDir)
    createcelfile_sh(cmdDic, args.linkedCelDir)

if __name__=='__main__':
    import argparse
    import time
    from datetime import datetime
    import subprocess
    import os
    parser = argparse.ArgumentParser()
    parser.add_argument('-tcf', '--targetCelFile',
            help='CEL file list.',
            default='cel_files.txt')
    parser.add_argument('-lf', '--logFile',
            help='log file',
            default='cel_files.{0}.log'.format(int(time.time())))
    parser.add_argument('-lcd', '--linkedCelDir',
            help='Directory for symbolic linked cel file',
            default='./')
    parser.add_argument('-rcd', '--rawCelDir',
            help='raw cel dir path for symbolic linking cel files',
            default='../')
    args = parser.parse_args()
    main(args)
