import time
from datetime import datetime
import subprocess
import os

def qc_report_parser(qc_report):
    qcDic = dict()
    for line in open(qc_report):
        if line.startswith('#'):
            continue
        #
        items = line.rstrip().split('\t')
        if items[0] in ['cel_files']:
            idxDic = dict()
            for idx, item in enumerate(items):
                if item in ['cel_files', 'axiom_dishqc_DQC']:
                    idxDic.setdefault(item, idx)
            continue
        #
        cel = items[idxDic['cel_files']]
        dqc = items[idxDic['axiom_dishqc_DQC']]
        qcDic.setdefault(cel, dqc)
    return qcDic

def idConvertor(idConvert):
    idDic = dict()
    for line in open(idConvert):
        items = line.strip().split('\t')
        idDic.setdefault(items[2], items[1])
    return idDic

def dqc_filter(qcDic, dqc_cut, idDic, outFile, linkedCelDir, fh_log):
    out = open(outFile, 'w')
    out.write('cel_files\n')
    filterout = 0
    save = 0
    for cel, dqc in qcDic.iteritems():
        if float(dqc) < float(dqc_cut):
            filterout += 1
            print >> fh_log, '#LOG {0} @ {1} @ {2} < {3} @ FILTEROUT'.format(idDic[cel], cel, dqc, dqc_cut)
        else:
            save += 1
            print >> fh_log, '#LOG {0} @ {1} @ {2} >= {3} @ SAVE'.format(idDic[cel], cel, dqc, dqc_cut)
            out.write('{0}/{1}\n'.format(linkedCelDir, idDic[cel]))
    print >> fh_log, '# N_FILTEROUT : {0}'.format(filterout)
    print >> fh_log, '# N_SAVE : {0}'.format(save)
    out.close()

def main(args):
    fh_log = open(args.logFile, 'w')
    print >> fh_log, args
    qcDic = qc_report_parser(args.qc_report)
    print >> fh_log, '# INPUT CEL : {0}'.format(len(qcDic))
    idDic = idConvertor(args.idConvert)
    dqc_filter(qcDic, args.dqc_cut, idDic, args.outFile, args.linkedCelDir, fh_log)


if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--qc-report')
    parser.add_argument('--idConvert')
    parser.add_argument('--linkedCelDir')
    parser.add_argument('--dqc-cut')
    parser.add_argument('--outFile')
    parser.add_argument('--logFile')
    args = parser.parse_args()
    main(args)
