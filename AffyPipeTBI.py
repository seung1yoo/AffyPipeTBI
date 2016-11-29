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

def check_script(path, script):
    if not os.path.isfile('{0}/{1}'.format(path, script)):
        print '#ERROR:check the {1} in {0}'.format(path, script)
        sys.exit()
    else:
        program = '{0}/{1}'.format(path, script)
    return program

def check_previous(outdir, checkfile):
    ## check the previous run
    if not os.path.isdir(outdir):
        os.mkdir(outdir)
        return 0
    else:
        if os.path.isfile(checkfile):
            print '''\
#WARING: {0} is alread exist. \
If you want re-run, delete {0} first and try again.\
            '''.format(checkfile)
            return 1
        else:
            return 0
        return 0
    return 0

def cel_files_exe(program, targetCelFile, rawCelDir, projectDir):
    linkedCelDir = '{0}/cel_files'.format(projectDir)
    mycellistfile = '{0}/mycellistfile.txt'.format(
            linkedCelDir)
    if check_previous(linkedCelDir, mycellistfile):
        return mycellistfile

    logFile = '{0}/log.cel_files'.format(projectDir)
    cmds = ['python2.7', program,
            '--targetCelFile', targetCelFile,
            '--rawCelDir', rawCelDir,
            '--linkedCelDir', linkedCelDir,
            '--logFile', logFile]
    print '#COMMAND:{0}'.format(' '.join(cmds))
    fd_popen = subprocess.Popen(cmds,
            stdout=subprocess.PIPE).stdout
    data = fd_popen.read().strip()
    fd_popen.close()

    return mycellistfile

def apt_geno_qc_exe(program, projectDir, analysisFile,
        xmlFile, analysisName, mycelFile):
    outDir = '{0}/apt-geno-qc'.format(projectDir)
    reportFile = '{0}/{1}.report.txt'.format(
            outDir, analysisName)
    if check_previous(outDir, reportFile):
        return reportFile

    logFile = '{0}/log.{1}'.format(projectDir, analysisName)
    cmds = [program,
            '--analysis-files-path', analysisFile,
            '--xml-file', xmlFile,
            '--cel-files', mycelFile,
            '--out-file', reportFile,
            '--log-file', logFile,
            '--verbose', '0',
            '--dm-out', '{0}/DM-out'.format(outDir)]
    print '#COMMAND:{0}'.format('\n  '.join(cmds))
    fd_popen = subprocess.Popen(cmds,
            stdout=subprocess.PIPE).stdout
    data = fd_popen.read().strip()
    fd_popen.close()

    return reportFile

def apt_genotype_axiom_exe(program, projectDir, analysisFile,
        xmlFile, analysisName, chipType, mycelFile):
    outDir = '{0}/apt-genotype-axiom'.format(projectDir)

    callFile = '{0}/{1}.calls.txt'.format(
            outDir, analysisName)
    posteriorsFile = '{0}/{1}.snp-posteriors.txt'.format(
                outDir, analysisName)
    alleleSummariesFile = '{0}/{1}.allele-summaries.txt'
            ''.format(outDir, analysisName)
    if check_previous(outDir, callFile):
        return callFile, posteriorsFile, alleleSummariesFile

    logFile = '{0}/log.{1}'.format(projectDir,
            analysisName)
    if analysisName in ['AxiomGT1']:
        cmds = [program,
                '--analysis-files-path', analysisFile,
                '--arg-file', xmlFile,
                '--out-dir', outDir,
                '--cel-files', mycelFile,
                '--log-file', logFile,
                '--snp-posteriors-output',
                '--snp-posteriors-output-file', posteriorsFile,
                '--allele-summaries',
                '--allele-summaries-file', alleleSummariesFile,
                '--chip-type', chipType,
                '--dual-channel-normalization',
                '--sketch-size', '50000']
    elif analysisName in ['AxiomSS1']:
        cmds = [program,
                '--analysis-files-path', analysisFile,
                '--arg-file', xmlFile,
                '--out-dir', outDir,
                '--cel-files', mycelFile,
                '--log-file', logFile,
                '--dual-channel-normalization']
    else:
        print '#ERROR:check ther analysis-name in configure'
        sys.exit()

    print '#COMMAND:{0}'.format('\n  '.join(cmds))
    fd_popen = subprocess.Popen(cmds,
            stdout=subprocess.PIPE).stdout
    data = fd_popen.read().strip()
    fd_popen.close()

    return callFile, posteriorsFile, alleleSummariesFile

def apt_format_result_exe(program, projectDir, callFile, annoFile, analysisName):
    outDir = '{0}/apt-format-result'.format(projectDir)
    pedFile = '{0}/{1}.plink.ped'.format(
            outDir, analysisName)
    mapFile = '{0}/{1}.plink.map'.format(
            outDir, analysisName)
    if check_previous(outDir, pedFile):
        return pedFile, mapFile
    logFile = '{0}/log.apt-format-result.{1}'.format(
            projectDir, analysisName)

    cmds = [program,
            '--log-file', logFile,
            '--calls-file', callFile,
            '--annotation-file', annoFile,
            '--snp-identifier-column', 'dbSNP_RS_ID',
            '--export-plink-file', '{0}/{1}.plink'.format(
                outDir, analysisName),
            '--export-plinkt-file', '{0}/{1}.plinkt'.format(
                outDir, analysisName),
            '--export-vcf-file', '{0}/{1}.vcf'.format(
                outDir, analysisName),
            '--export-txt-file', '{0}/{1}.txt'.format(
                outDir, analysisName),
            '--export-call-format', 'base_call']
            #'--annotation-columns', 'Affy_SNP_ID,dbSNP_RS_ID,dbSNP_Loctype,Chromosome,Physical_Position,Position_End,Strand,Allele_A,Allele_B,Ref_Allele,Alt_Allele,Associated_Gene']

    print '#COMMAND:{0}'.format('\n  '.join(cmds))
    fd_popen = subprocess.Popen(cmds,
            stdout=subprocess.PIPE).stdout
    data = fd_popen.read().strip()
    fd_popen.close()

    return pedFile, mapFile

def ped_confirm(program, plink, pedFile, mapFile, projectDir):
    outDir = '{0}/apt-format-result'.format(projectDir)
    prefix = pedFile.split('.ped')[0]
    new_pedFile = '{0}.make-bed.record.ped'.format(prefix)
    new_mapFile = '{0}.make-bed.record.map'.format(prefix)
    if check_previous(outDir, new_pedFile):
        return new_pedFile, new_mapFile
    logFile = '{0}/log.ped_confirm'.format(projectDir)
    cmds = ['python2.7', program,
            '--plink', plink,
            '--ped', pedFile,
            '--map', mapFile,
            '--prefix', prefix,
            '--logfile', logFile]
    print '#COMMAND:{0}'.format('\n  '.join(cmds))
    fd_popen = subprocess.Popen(cmds,
            stdout=subprocess.PIPE).stdout
    data = fd_popen.read().strip()
    fd_popen.close()
    return new_pedFile, new_mapFile


def main(args):
    #print args
    configDic = config_file_parser(args.config)

    ## cel_files execute
    program = check_script(configDic['affyPipeTBI_path'],
            'cel_files.py')
    mycellistfile = cel_files_exe(program,
            configDic['project_cel_files'],
            configDic['raw_cel_path'],
            configDic['project_home_path'])

    ## QC (apt-geno-qc)
    program = check_script(configDic['apt_path'],
            'apt-geno-qc')
    qc_reportFile = apt_geno_qc_exe(program,
            configDic['project_home_path'],
            configDic['analysis-files-path'],
            configDic['xml-file-QC1'],
            configDic['analysis-name-QC1'],
            mycellistfile)

    ## Genotype Calling (apt-genotype-axiom)
    program = check_script(configDic['apt_path'],
            'apt-genotype-axiom')
    callFile_gt1, posteriorsFile_gt1, alleleSummariesFile_gt1 = apt_genotype_axiom_exe(program,
            configDic['project_home_path'],
            configDic['analysis-files-path'],
            configDic['xml-file-GT1'],
            configDic['analysis-name-GT1'],
            configDic['chip-type'],
            mycellistfile)

    ## Signature SNPs (apt-genotype-axiom)
    program = check_script(configDic['apt_path'],
            'apt-genotype-axiom')
    callFile_ss1, posteriorsFile_ss1, alleleSummariesFile_ss1 = apt_genotype_axiom_exe(program,
            configDic['project_home_path'],
            configDic['analysis-files-path'],
            configDic['xml-file-SS1'],
            configDic['analysis-name-SS1'],
            configDic['chip-type'],
            mycellistfile)

    ## Make PLINK, VCF, TXT files (apt-format-result)
    program = check_script(configDic['apt_path'],
            'apt-format-result')
    pedFile, mapFile = apt_format_result_exe(program,
            configDic['project_home_path'],
            callFile_gt1,
            configDic['annotation-file'],
            configDic['analysis-name-GT1'])

    plink = check_script(configDic['plink_path'],
            'plink')
    program = check_script(configDic['affyPipeTBI_path'],
            'ped_confirm.py')
    pedFile, mapFile = ped_confirm(program, plink,
            pedFile, mapFile, configDic['project_home_path'])

    ## SNPolisher








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
