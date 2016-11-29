
def main(args):

    log_out = open(args.logfile, 'w')

    cmds = [args.plink,
            '--ped', args.ped,
            '--map', args.map,
            '--make-bed',
            '--out', '{0}.make-bed'.format(args.prefix),
            '--no-fid --no-parents --no-pheno --no-sex']
    print >> log_out, ' '.join(cmds)
    os.system(' '.join(cmds))
    
    cmds = [args.plink,
            '--bfile', '{0}.make-bed'.format(args.prefix),
            '--recode',
            '--out', '{0}.make-bed.record'.format(args.prefix)]
    print >> log_out, ' '.join(cmds)
    os.system(' '.join(cmds))

    log_out.close()

if __name__=='__main__':
    import os
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--plink')
    parser.add_argument('--ped')
    parser.add_argument('--map')
    parser.add_argument('--prefix')
    parser.add_argument('--logfile')
    args = parser.parse_args()
    main(args)
