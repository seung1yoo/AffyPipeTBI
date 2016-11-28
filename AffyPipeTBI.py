def config_file_parser(config_file):
    configDic = dict()
    for line in open(config_file):
        if line.startswith('#'):
            continue
        if not line.strip():
            continue
        items = line.strip().split('=')
        items = [x.strip() for x in items]
        configDic.setdefault(items[0], items[1])

    for key, value in configDic.iteritems():
        print '#Configuration : {0} -> {1}'.format(key, value)
    return configDic

def cel_files_exe(program, targetCelFile, rawCelDir, projectDir):
    linkedCelDir = '{0}/cel_files'.format(projectDir)
    if not os.path.isdir(linkedCelDir):
        os.mkdir(linkedCelDir)
    logFile = '{0}/log.cel_files'.format(projectDir)
    cmds = ['python2.7', program,
            '--targetCelFile', targetCelFile,
            '--rawCelDir', rawCelDir,
            '--linkedCelDir', linkedCelDir,
            '--logFile', logFile]
    fd_popen = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout
    data = fd_popen.read().strip()
    fd_popen.close()

    mycellistfile = '{0}/cel_files/mycellistfile.txt'.format(projectDir)
    if not os.path.isfile(mycellistfile):
        print '#ERROR:check the {0}'.format(mycellistfile)
        sys.exit()

    return mycellistfile




def main(args):
    #print args
    configDic = config_file_parser(args.config)

    ## cel_files execute
    if not os.path.isfile('{0}/cel_files.py'.format(\
        configDic['affyPipeTBI_path'])):
        print '#ERROR:check the cel_files.py in {0}'.format(\
                configDic['affyPipeTBI_path'])
        sys.exit()
    else:
        program = '{0}/cel_files.py'.format(configDic['affyPipeTBI_path'])


    mycellistfile = cel_files_exe(program, configDic['project_cel_files'],
                                  configDic['raw_cel_path'],
                                  configDic['project_home_path'])



if __name__=='__main__':
    import os
    import sys
    import subprocess
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='config file name',
            default='/BiO/BioPeople/siyoo/Axiom/Scripts/AffyPipeTBI.conf')
    args = parser.parse_args()
    main(args)
