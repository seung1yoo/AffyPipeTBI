
def main(args):
    print args

if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--program',
            default='/BiO/BioPeople/siyoo/Axiom/Tools/apt-1.19.0-x86_64-intel-linux/bin/apt-genotype-axiom')
    parser.add_argument('--analysis-files-path',
            default='/BiO/BioPeople/siyoo/Axiom/Libraries/Axiom_PMRA')
    parser.add_argument('--arg-file',
            default='/BiO/BioPeople/siyoo/Axiom/Libraries/Axiom_PMRA/Axiom_PMRA_96orMore_Step2.r1.apt-genotype-axiom.AxiomGT1.apt2.xml')
    parser.add_argument('--out-dir',
            default='/BiOfs/BioProjects/AMORE-Axiom-20161123/apt-genotype-axiom-GT1-out')
    parser.add_argument('--cel-files',
            default='/BiOfs/BioProjects/AMORE-Axiom-20161123/celFiles/mycellistfile.txt')
    parser.add_argument('--log-file',
            default='/BiOfs/BioProjects/AMORE-Axiom-20161123/apt-genotype-axiom-GT1-log.txt')
    parser.add_argument('--snp-posteriors-output-file',
            default='/BiOfs/BioProjects/AMORE-Axiom-20161123/apt-genotype-axiom-GT1-out/AxiomGT1.snp-posteriors.txt')
    parser.add_argument('--allele-summaries-file',
            default='/BiOfs/BioProjects/AMORE-Axiom-20161123/apt-genotype-axiom-GT1-out/AxiomGT1.allele-summaries.txt')
    parser.add_argument('--chip-type',
            default='Axiom_PMRA.r1')
    args = parser.parse_args()
    main(args)



#/BiO/BioPeople/siyoo/Axiom/Tools/apt-1.19.0-x86_64-intel-linux/bin/apt-genotype-axiom \
#--analysis-files-path /BiO/BioPeople/siyoo/Axiom/Libraries/Axiom_PMRA \
#--arg-file /BiO/BioPeople/siyoo/Axiom/Libraries/Axiom_PMRA/Axiom_PMRA_96orMore_Step2.r1.apt-genotype-axiom.AxiomGT1.apt2.xml \
#--out-dir /BiOfs/BioProjects/AMORE-Axiom-20161123/apt-genotype-axiom-GT1-out \
#--cel-files /BiOfs/BioProjects/AMORE-Axiom-20161123/celFiles/mycellistfile.txt \
#--log-file /BiOfs/BioProjects/AMORE-Axiom-20161123/apt-genotype-axiom-GT1-log.txt \
#--snp-posteriors-output \
#--snp-posteriors-output-file /BiOfs/BioProjects/AMORE-Axiom-20161123/apt-genotype-axiom-GT1-out/AxiomGT1.snp-posteriors.txt \
#--allele-summaries \
#--allele-summaries-file /BiOfs/BioProjects/AMORE-Axiom-20161123/apt-genotype-axiom-GT1-out/AxiomGT1.allele-summaries.txt \
#--chip-type Axiom_PMRA.r1 \
#--dual-channel-normalization \
#--sketch-size 50000
