import time
from datetime import datetime
import subprocess
import os

def qc_report_parser(reportFile):
    qcDic = dict()
    for line in open(reportFile):
        if line.startswith('#'):
            continue
        #
        items = line.rstrip().split('\t')
        if items[0] in ['cel_files']:
            idxDic = dict()
            for idx, item in enumerate(items):
                if item in ['cel_files', 'call_rate']:
                    idxDic.setdefault(item, idx)
            continue
        #
        cel = items[idxDic['cel_files']]
        cr = items[idxDic['call_rate']]
        qcDic.setdefault(cel, cr)
    return qcDic

def cr_filter(qcDic, callrate_cut, mycellistfile_cr, linkedCelDir, fh_log):
    out = open(mycellistfile_cr, 'w')
    out.write('cel_files\n')
    filterout = 0
    save = 0
    for cel, cr in qcDic.iteritems():
        if float(cr) < float(callrate_cut):
            filterout += 1
            print >> fh_log, '#LOG {0} @ {1} < {2} @ FILTEROUT'.format(cel, cr, callrate_cut)
        else:
            save += 1
            print >> fh_log, '#LOG {0} @ {1} >= {2} @ SAVE'.format(cel, cr, callrate_cut)
            out.write('{0}/{1}\n'.format(linkedCelDir, cel))
    print >> fh_log, '# N_FILTEROUT : {0}'.format(filterout)
    print >> fh_log, '# N_SAVE : {0}'.format(save)
    out.close()

def main(args):
    fh_log = open(args.logFile, 'w')
    print >> fh_log, args
    print >> fh_log, '# callrate_cut : {0}'.format(args.callrate_cut)
    #
    qcDic = qc_report_parser(args.reportFile)
    cr_filter(qcDic, args.callrate_cut, args.mycellistfile_cr, args.linkedCelDir, fh_log)


    fh_log.close()

if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--reportFile')
    parser.add_argument('--linkedCelDir')
    parser.add_argument('--callrate_cut')
    parser.add_argument('--mycellistfile_cr')
    parser.add_argument('--logFile')
    args = parser.parse_args()
    main(args)
