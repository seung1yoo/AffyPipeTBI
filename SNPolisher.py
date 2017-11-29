
def main(args):
    print args
    log_out = open(args.logFile, 'w')

    if args.species in ['Human']:
        speciesType = 'Human'
    elif args.species in ['non-Human']:
        speciesType = 'diploid'
    elif args.species in ['diploid']:
        speciesType = 'diploid'
    elif args.species in ['polyploid']:
        speciesType = 'polyploid'
    else:
        speciesType = 'diploid'
        speciesType = 'polyploid'

    r_scripts = [
        "setwd('{0}')".format(args.workingDir),
         "library(methods)",
         "if (is.element('SNPolisher',installed.packages())){",
         "library(SNPolisher)}else{",
         "install.packages('%s',repos=NULL,type='source');library(SNPolisher)}" % (args.snpolisher),
         "ps.metrics <- Ps_Metrics(posteriorFile=paste('{1}'),callFile=paste('{2}'),output.metricsFile=paste('{0}','Ps_metrics.txt',sep='/'))".format(args.workingDir, args.posteriorsFile, args.callFile),
         "Ps_Classification(metricsFile=paste('{0}','Ps_metrics.txt',sep='/'),ps2snpFile=paste('{1}',sep=''),output.dir=paste('{0}',sep='/'),SpeciesType='{2}')".format(args.workingDir, args.ps2snpFile, speciesType),
         "OTV_Caller(summaryFile='{0}', posteriorFile='{1}', callFile='{2}', confidenceFile='{3}', pidFile='{4}/OffTargetVariant.ps', output.dir='{4}/OTV', OTV.only=TRUE)".format(args.summaryFile, args.posteriorsFile, args.callFile, args.confidenceFile, args.workingDir),
         "print('ENDOK')"]

    out_r = open('{0}/SNPolisher.R'.format(args.workingDir), 'w')
    for r_script in r_scripts:
        out_r.write('{0}\n'.format(r_script))
        print >> log_out, r_script
    out_r.close()

    cmds = [args.r,
            'CMD',
            'BATCH',
            '{0}/SNPolisher.R'.format(args.workingDir)]
    print >> log_out, ' '.join(cmds)
    os.system(' '.join(cmds))

    log_out.close()

if __name__=='__main__':
    import os
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--r')
    parser.add_argument('--snpolisher')
    parser.add_argument('--workingDir')
    parser.add_argument('--posteriorsFile')
    parser.add_argument('--callFile')
    parser.add_argument('--summaryFile')
    parser.add_argument('--confidenceFile')
    parser.add_argument('--ps2snpFile')
    parser.add_argument('--species')
    parser.add_argument('--logFile')
    args = parser.parse_args()
    main(args)
