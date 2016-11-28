

def main(args):
    print args


if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--program',
            default='/BiO/BioPeople/siyoo/Axiom/Tools/apt-1.19.0-x86_64-intel-linux/bin/apt-geno-qc')
    parser.add_argument('--project-path',
            default='/BiOfs/BioProjects/AMORE-Axiom-20161123/')
    parser.add_argument('--analysis-files-path',
            default='/BiO/BioPeople/siyoo/Axiom/Libraries/Axiom_PMRA')
    parser.add_argument('--xml-file',
            default='/BiO/BioPeople/siyoo/Axiom/Libraries/Axiom_PMRA/Axiom_PMRA.r1.apt-geno-qc.AxiomQC1.xml')
    parser.add_argument('--cel-files',
            default='/BiOfs/BioProjects/AMORE-Axiom-20161123/celFiles/mycellistfile.txt')
    parser.add_argument('--out-file',
            default='/BiOfs/BioProjects/AMORE-Axiom-20161123/apt-geno-qc_QC1-out/apt-geno-qc.report.txt')
    parser.add_argument('--dm-out',
            default='/BiOfs/BioProjects/AMORE-Axiom-20161123/apt-geno-qc_QC1-out/DM-out')
    args = parser.parse_args()
    main(args)

#/BiO/BioPeople/siyoo/Axiom/Tools/apt-1.19.0-x86_64-intel-linux/bin/apt-geno-qc \
#--analysis-files-path /BiO/BioPeople/siyoo/Axiom/Libraries/Axiom_PMRA \
#--xml-file /BiO/BioPeople/siyoo/Axiom/Libraries/Axiom_PMRA/Axiom_PMRA.r1.apt-geno-qc.AxiomQC1.xml \
#--cel-files /BiOfs/BioProjects/AMORE-Axiom-20161123/celFiles/mycellistfile.txt \
#--out-file /BiOfs/BioProjects/AMORE-Axiom-20161123/apt-geno-qc_QC1-out/apt-geno-qc.report.txt \
#--dm-out /BiOfs/BioProjects/AMORE-Axiom-20161123/apt-geno-qc_QC1-out/DM-out
