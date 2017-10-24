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
        print '#CONFIGRATION : {0} -> {1}'.format(key, value)
    return configDic

def check_script(path, script):
    if not os.path.isfile('{0}/{1}'.format(path, script)):
        print '#CHECK_SCRIPT : the {1} in {0} NO'.format(path, script)
        sys.exit()
    else:
        print '#CHECK_SCRIPT : the {1} in {0} OK'.format(path, script)
        program = '{0}/{1}'.format(path, script)
    return program

def check_previous_run(outdir, checkfile):
    ## check the previous run
    if not os.path.isdir(outdir):
        os.mkdir(outdir)
        return 0
    else:
        if os.path.isfile(checkfile):
            print '#CHECK_PREVIOUS_RUN (1/3) : {0} is alread exist.'.format(checkfile)
            print '#CHECK_PREVIOUS_RUN (2/3) : If you want re-run, delete {0} and re-run.'.format(checkfile)
            print '#CHECK_PREVIOUS_RUN (3/3) : This step is jumped.'
            return 1
        else:
            return 0
        return 0
    return 0

def cel_collector(program, targetCelFile, rawCelDir, projectDir):
    linkedCelDir = '{0}/cel_files'.format(projectDir)
    mycellistfile = '{0}/mycellistfile.txt'.format(linkedCelDir)
    idConvertedFile = '{0}/convertedID.xls'.format(linkedCelDir)
    logFile = '{0}/log.cel_files'.format(projectDir)

    if check_previous_run(linkedCelDir, mycellistfile):
        return mycellistfile, linkedCelDir, idConvertedFile

    cmds = ['python2.7', program,
            '--targetCelFile', targetCelFile,
            '--rawCelDir', rawCelDir,
            '--linkedCelDir', linkedCelDir,
            '--logFile', logFile]
    print '#COMMAND:{0}'.format(' '.join(cmds))
    fd_popen = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout
    data = fd_popen.read().strip()
    fd_popen.close()

    return mycellistfile, linkedCelDir, idConvertedFile

def apt_geno_qc_exe(program, projectDir, analysisFile, xmlFile, analysisName, mycelFile):
    outDir = '{0}/apt-geno-qc'.format(projectDir)
    reportFile = '{0}/{1}.report.txt'.format(outDir, analysisName)
    logFile = '{0}/log.{1}'.format(projectDir, analysisName)

    if check_previous_run(outDir, reportFile):
        return reportFile

    cmds = [program,
            '--analysis-files-path', analysisFile,
            '--xml-file', xmlFile,
            '--cel-files', mycelFile,
            '--out-file', reportFile,
            '--log-file', logFile,
            '--verbose', '0',
            '--dm-out', '{0}/DM-out'.format(outDir)]
    print '#COMMAND:{0}'.format(' '.join(cmds))
    fd_popen = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout
    data = fd_popen.read().strip()
    fd_popen.close()

    return reportFile

def dqc_filter(program, qc_reportFile, idConvertedFile, linkedCelDir, projectDir, dqc_cut):
    dqc_Dir = '{0}/dqc_filter'.format(projectDir)
    mycellistfile_dqc = '{0}/mycellistfile.dqc.txt'.format(dqc_Dir)
    logFile = '{0}/log.dqc_filter'.format(projectDir)

    if check_previous_run(dqc_Dir, mycellistfile_dqc):
        return mycellistfile_dqc

    cmds = ['python2.7', program,
            '--qc-report', qc_reportFile,
            '--idConvert', idConvertedFile,
            '--linkedCelDir', linkedCelDir,
            '--dqc-cut', dqc_cut,
            '--outFile', mycellistfile_dqc,
            '--logFile', logFile]
    print '#COMMAND:{0}'.format(' '.join(cmds))
    fd_popen = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout
    data = fd_popen.read().strip()
    fd_popen.close()

    return mycellistfile_dqc

def apt_genotype_axiom_exe(program, projectDir, analysisFile, xmlFile, analysisName, chipType, mycelFile, analysisType):
    outDir = '{0}/apt-genotype-axiom_{1}'.format(projectDir, analysisType)
    callFile = '{0}/{1}.calls.txt'.format(outDir, analysisName)
    posteriorsFile = '{0}/{1}.snp-posteriors.txt'.format(outDir, analysisName)
    alleleSummariesFile = '{0}/{1}.allele-summaries.txt'.format(outDir, analysisName)
    reportFile = '{0}/{1}.report.txt'.format(outDir, analysisName)
    logFile = '{0}/log.{1}'.format(projectDir, analysisName)

    if check_previous_run(outDir, callFile):
        return callFile, posteriorsFile, alleleSummariesFile, reportFile

    if analysisName in ['AxiomGT1_1', 'AxiomGT1_2']:
        cmds = [program,
                '--analysis-files-path', analysisFile,
                '--arg-file', xmlFile,
                '--out-dir', outDir,
                '--cel-files', mycelFile,
                '--log-file', logFile,
                '--analysis-name', analysisName,
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
                '--analysis-name', analysisName,
                '--dual-channel-normalization']
    else:
        print '#ERROR:check ther analysis-name in configure file.'
        sys.exit()

    print '#COMMAND:{0}'.format(' '.join(cmds))
    fd_popen = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout
    data = fd_popen.read().strip()
    fd_popen.close()

    return callFile, posteriorsFile, alleleSummariesFile, reportFile

def callrate_filter(program, reportFile, linkedCelDir, projectDir, callrate_cut):
    callrate_Dir = '{0}/callrate_filter'.format(projectDir)
    mycellistfile_cr = '{0}/mycellistfile.cr.txt'.format(callrate_Dir)
    logFile = '{0}/log.callrate_filter'.format(projectDir)

    if check_previous_run(callrate_Dir, mycellistfile_cr):
        return mycellistfile_cr

    cmds = ['python2.7', program,
            '--reportFile', reportFile,
            '--linkedCelDir', linkedCelDir,
            '--callrate_cut', callrate_cut,
            '--mycellistfile_cr', mycellistfile_cr,
            '--logFile', logFile]
    print '#COMMAND:{0}'.format(' '.join(cmds))
    fd_popen = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout
    data = fd_popen.read().strip()
    fd_popen.close()

    return mycellistfile_cr

def apt_format_result_exe(program, projectDir, callFile, annoFile, analysisName):
    outDir = '{0}/apt-format-result'.format(projectDir)
    pedFile = '{0}/{1}.plink.ped'.format(outDir, analysisName)
    mapFile = '{0}/{1}.plink.map'.format(outDir, analysisName)
    vcfFile = '{0}/{1}.vcf'.format(outDir, analysisName)
    txtFile = '{0}/{1}.txt'.format(outDir, analysisName)
    logFile = '{0}/log.apt-format-result.{1}'.format(projectDir, analysisName)

    if check_previous_run(outDir, pedFile):
        return pedFile, mapFile, vcfFile, txtFile

    cmds = [program,
            '--log-file', logFile,
            '--calls-file', callFile,
            '--annotation-file', annoFile,
            '--snp-identifier-column', 'probeset_id',
            '--export-plink-file', '{0}/{1}.plink'.format(outDir, analysisName),
            '--export-plinkt-file', '{0}/{1}.plinkt'.format(outDir, analysisName),
            '--export-vcf-file', '{0}/{1}.vcf'.format(outDir, analysisName),
            '--export-txt-file', '{0}/{1}.txt'.format(outDir, analysisName),
            '--export-call-format', 'base_call']
    print '#COMMAND:{0}'.format(' '.join(cmds))
    fd_popen = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout
    data = fd_popen.read().strip()
    fd_popen.close()

    return pedFile, mapFile, vcfFile, txtFile

def ped_confirm_exe(program, plink, pedFile, mapFile, projectDir):
    outDir = '{0}/apt-format-result'.format(projectDir)
    prefix = pedFile.split('.ped')[0]
    new_pedFile = '{0}.make-bed.record.ped'.format(prefix)
    new_mapFile = '{0}.make-bed.record.map'.format(prefix)
    logFile = '{0}/log.ped_confirm'.format(projectDir)

    if check_previous_run(outDir, new_pedFile):
        return new_pedFile, new_mapFile

    cmds = ['python2.7', program,
            '--plink', plink,
            '--ped', pedFile,
            '--map', mapFile,
            '--prefix', prefix,
            '--logfile', logFile]
    print '#COMMAND:{0}'.format(' '.join(cmds))
    fd_popen = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout
    data = fd_popen.read().strip()
    fd_popen.close()

    return new_pedFile, new_mapFile

def snpolisher_exe(program, projectDir, snpolisher, rPath, posteriorsFile, callFile, ps2snpFile, species):
    outDir = '{0}/SNPolisher'.format(projectDir)
    performanceFile = '{0}/Ps.performance.txt'.format(outDir)
    logFile = '{0}/log.SNPolisher'.format(projectDir)

    if check_previous_run(outDir, performanceFile):
        return performanceFile

    cmds = ['python2.7', program,
            '--snpolisher', snpolisher,
            '--workingDir', outDir,
            '--r', rPath,
            '--posteriorsFile', posteriorsFile,
            '--callFile', callFile,
            '--ps2snpFile', ps2snpFile,
            '--logFile', logFile,
            '--species', species]
    print '#COMMAND:{0}'.format('\n  '.join(cmds))
    fd_popen = subprocess.Popen(cmds, stdout=subprocess.PIPE).stdout
    data = fd_popen.read().strip()
    fd_popen.close()

    return performanceFile

def main(args):
    #print args
    configDic = config_file_parser(args.config)

    ## cel_collector execute
    program = check_script(configDic['affyPipeTBI_path'],
            'cel_collector.py')
    mycellistfile, linkedCelDir, idConvertedFile = cel_collector(
            program,
            configDic['project_cel_files'],
            configDic['raw_cel_path'],
            configDic['project_home_path'])
    tbi_uploader.cel(idConvertedFile, linkedCelDir,
            '{0}/00_CEL_files'.format(configDic['project_result']))

    ## QC (apt-geno-qc)
    program = check_script(configDic['apt_path'],
            'apt-geno-qc')
    qc_reportFile = apt_geno_qc_exe(program,
            configDic['project_home_path'],
            configDic['analysis-files-path'],
            configDic['xml-file-QC1'],
            configDic['analysis-name-QC1'],
            mycellistfile)
    qc_reportFile = tbi_idConvertor.cel_col(qc_reportFile, configDic['project_id'], '\t', 0, idConvertedFile)
    tbi_uploader.aFileSymlinker(qc_reportFile, 'Axiom.QC.report.txt', '{0}/01_QC_report'.format(configDic['project_result']))

    ## DQC filter ()
    program = check_script(configDic['affyPipeTBI_path'],
            'dqc_filter.py')
    mycellistfile_dqc = dqc_filter(program,
            qc_reportFile,
            idConvertedFile,
            linkedCelDir,
            configDic['project_home_path'],
            configDic['dqc_cut'])

    ## Genotype Calling (apt-genotype-axiom)
    program = check_script(configDic['apt_path'],
            'apt-genotype-axiom')
    callFile_gt1, posteriorsFile_gt1, alleleSummariesFile_gt1, reportFile_gt1 = apt_genotype_axiom_exe(program,
            configDic['project_home_path'],
            configDic['analysis-files-path'],
            configDic['xml-file-GT1_1'],
            configDic['analysis-name-GT1_1'],
            configDic['chip-type'],
            mycellistfile_dqc,
            'STEP1')
    ## Call_rate filter
    program = check_script(configDic['affyPipeTBI_path'],
            'callrate_filter.py')
    mycellistfile_cr = callrate_filter(program,
            reportFile_gt1,
            linkedCelDir,
            configDic['project_home_path'],
            configDic['callrate_cut'])
    ## Genotype Calling (apt-genotype-axiom)
    program = check_script(configDic['apt_path'],
            'apt-genotype-axiom')
    callFile_gt1, posteriorsFile_gt1, alleleSummariesFile_gt1, reportFile_gt1 = apt_genotype_axiom_exe(program,
            configDic['project_home_path'],
            configDic['analysis-files-path'],
            configDic['xml-file-GT1_2'],
            configDic['analysis-name-GT1_2'],
            configDic['chip-type'],
            mycellistfile_cr,
            'STEP2')
    reportFile_gt1 = tbi_idConvertor.cel_col(reportFile_gt1, configDic['project_id'], '\t', 0, idConvertedFile)
    tbi_uploader.aFileSymlinker(reportFile_gt1, 'Genotype.QC.report.txt', '{0}/01_QC_report'.format(configDic['project_result']))

    ## Signature SNPs (apt-genotype-axiom)
    program = check_script(configDic['apt_path'],
            'apt-genotype-axiom')
    callFile_ss1, posteriorsFile_ss1, alleleSummariesFile_ss1, reportFile_ss1 = apt_genotype_axiom_exe(program,
            configDic['project_home_path'],
            configDic['analysis-files-path'],
            configDic['xml-file-SS1'],
            configDic['analysis-name-SS1'],
            configDic['chip-type'],
            mycellistfile_cr,
            'SignatureSNP')

    ## Make PLINK, VCF, TXT files (apt-format-result)
    program = check_script(configDic['apt_path'],
            'apt-format-result')
    pedFile, mapFile, vcfFile, txtFile = apt_format_result_exe(program,
            configDic['project_home_path'],
            callFile_gt1,
            configDic['annotation-file'],
            configDic['analysis-name-GT1_2'])

    vcfFile = tbi_idConvertor.cel_title(vcfFile, configDic['project_id'], '\t', str('#CHROM'), idConvertedFile)
    vcfFile = tbi_idConvertor.snpId_col(vcfFile, configDic['project_id'], '\t', 2, configDic['anno-file-csv'], 2)
    tbi_uploader.aFileSymlinker(vcfFile, 'Genotype.vcf', '{0}/02_Genotype'.format(configDic['project_result']))

    txtFile = tbi_idConvertor.cel_title(txtFile, configDic['project_id'], '\t', str('probeset_id'), idConvertedFile)
    txtFile = tbi_idConvertor.snpId_col(txtFile, configDic['project_id'], '\t', 0, configDic['anno-file-csv'], 2)
    tbi_uploader.aFileSymlinker(txtFile, 'Genotype.txt', '{0}/02_Genotype'.format(configDic['project_result']))

    plink = check_script(configDic['plink_path'], 'plink')
    program = check_script(configDic['affyPipeTBI_path'], 'ped_confirm.py')
    pedFile, mapFile = ped_confirm_exe(program, plink, pedFile, mapFile, configDic['project_home_path'])

    mapFile = tbi_idConvertor.snpId_col(mapFile, configDic['project_id'], '\t', 1, configDic['anno-file-csv'], 2)
    tbi_uploader.aFileSymlinker(mapFile, 'Genotype.map', '{0}/03_Plink'.format(configDic['project_result']))

    pedFile = tbi_idConvertor.cel_col(pedFile, configDic['project_id'], ' ', 0, idConvertedFile)
    pedFile = tbi_idConvertor.cel_col(pedFile, configDic['project_id'], ' ', 1, idConvertedFile)
    tbi_uploader.aFileSymlinker(pedFile, 'Genotype.ped', '{0}/03_Plink'.format(configDic['project_result']))

    ## SNPolisher
    program = check_script(configDic['affyPipeTBI_path'],
            'SNPolisher.py')
    performanceFile = snpolisher_exe(program,
                   configDic['project_home_path'],
                   configDic['SNPolisher_path'],
                   configDic['R_path'],
                   posteriorsFile_gt1,
                   callFile_gt1,
                   configDic['ps2snp-file'],
                   configDic['species'])

    ## Part of Results list
    print '##### RESULTs list #####'
    print '## CEL collector ##'
    print '#RESULTs : mycellistfile : {0}'.format(mycellistfile)
    print '#RESULTs : linkedCelDir : {0}'.format(linkedCelDir)
    print '## QC ##'
    print '#RESULTs : qc_reportFile : {0}'.format(qc_reportFile)
    print '## CALLING ##'
    print '#RESULTs : callFile_gt1 : {0}'.format(callFile_gt1)
    print '#RESULTs : posteriorsFile_gt1 : {0}'.format(posteriorsFile_gt1)
    print '#RESULTs : alleleSummariesFile_gt1 : {0}'.format(alleleSummariesFile_gt1)
    print '#RESULTs : reportFile_gt1 : {0}'.format(reportFile_gt1)
    print '#RESULTs : callFile_ss1 : {0}'.format(callFile_ss1)
    print '#RESULTs : posteriorsFile_ss1 : {0}'.format(posteriorsFile_ss1)
    print '#RESULTs : alleleSummariesFile_ss1 : {0}'.format(alleleSummariesFile_ss1)
    print '#RESULTs : reportFile_ss1 : {0}'.format(reportFile_ss1)
    print '## FORMATTING ##'
    print '#RESULTs : pedFile : {0}'.format(pedFile)
    print '#RESULTs : mapFile : {0}'.format(mapFile)
    print '#RESULTs : vcfFile : {0}'.format(vcfFile)
    print '#RESULTs : txtFile : {0}'.format(txtFile)
    print '## SNPolisher ##'
    print '#RESULTs : performanceFile : {0}'.format(performanceFile)

    print '################################'
    print '# AffyPipeTBI is done          #'
    print '# seungil.yoo@theragenetex.com #'
    print '################################'

if __name__=='__main__':
    import os
    import sys
    import subprocess
    import argparse
    import tbi_uploader
    import tbi_idConvertor
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='config file name',
            default='/BiO/BioPeople/siyoo/Axiom/Scripts/AffyPipeTBI.conf')
    args = parser.parse_args()
    main(args)
