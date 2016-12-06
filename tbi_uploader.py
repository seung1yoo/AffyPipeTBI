def files_linker(files, path, out_log):
    if not os.path.isdir(path):
        cmd = ['mkdir', '-p', path]
        print >> out_log, ' '.join(cmd)
        os.system(' '.join(cmd))

    for file in files:
        targetFile = '{0}/{1}'.format(path, file.split('/')[-1])
        try:
            print >> out_log, '#symlink : {0} -> {1}'.format(file, targetFile)
            os.symlink(file, targetFile)
        except OSError as e:
            print >> out_log, '#symlink : {0}'.format(e)

def main(args):
    out_log = open(args.logFile, 'w')

    # Result dir making
    if not os.path.isdir(args.outDir):
        cmd = ['mkdir', args.outDir]
        print >> out_log, ' '.join(cmd)
        os.system(' '.join(cmd))

    # making 00_CEL_files
    try:
        print >> out_log, '#symlink : {0} -> {1}'.format(args.celFilesDir, '{0}/00_CEL_files'.format(args.outDir))
        os.symlink(args.celFilesDir, '{0}/00_CEL_files'.format(args.outDir))
    except OSError as e:
        print >> out_log, '#symlink : {0}'.format(e)

    # making 01_QC_report
    qcReportDir = '{0}/01_QC_report'.format(args.outDir)
    files_linker(args.qcReports, qcReportDir, out_log)

    # making 02_Genotype
    genotypeDir = '{0}/02_Genotype'.format(args.outDir)
    files_linker(args.genotypes, genotypeDir, out_log)

    # making 03_plink
    plinkDir = '{0}/03_plink'.format(args.outDir)
    files_linker(args.plinks, plinkDir, out_log)

    # sample cel file
    targetFile = '{0}/{1}'.format(args.outDir, args.celFile.split('/')[-1])
    try:
        print >> out_log, '#symlink : {0} -> {1}'.format(args.celFile, targetFile)
        os.symlink(args.celFile, targetFile)
    except OSError as e:
        print >> out_log, '#symlink : {0}'.format(e)

    out_log.close()

if __name__=='__main__':
    import os
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--outDir')
    parser.add_argument('-c', '--celFilesDir')
    parser.add_argument('-q', '--qcReports', nargs='+')
    parser.add_argument('-g', '--genotypes', nargs='+')
    parser.add_argument('-p', '--plinks', nargs='+')
    parser.add_argument('--celFile')
    parser.add_argument('-l', '--logFile')
    args = parser.parse_args()
    main(args)
