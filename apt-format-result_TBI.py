def main(args):
    print args

if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--program',
            default='/BiO/BioPeople/siyoo/Axiom/Tools/apt-1.19.0-x86_64-intel-linux/bin/apt-format-result')
    parser.add_argument('--calls-file',
            default='/BiOfs/BioProjects/AMORE-Axiom-20161123/apt-genotype-axiom-out/AxiomGT1.calls.txt')
    parser.add_argument('--annotation-file',
            default='/BiO/BioPeople/siyoo/Axiom/Libraries/Axiom_PMRA/Axiom_PMRA.na35.annot.db')
    parser.add_argument('--snp-identifier-column', choices=('dbSNP_RS_ID', 'probeset_id'),
            default='dbSNP_RS_ID')
    parser.add_argument('--export-plink-file',
            default='/BiOfs/BioProjects/AMORE-Axiom-20161123/apt-format-result-out/AxiomGT1.plink')
    parser.add_argument('--export-plinkt-file',
            default='/BiOfs/BioProjects/AMORE-Axiom-20161123/apt-format-result-out/AxiomGT1.plinkt')
    parser.add_argument('--export-vcf-file',
            default='/BiOfs/BioProjects/AMORE-Axiom-20161123/apt-format-result-out/AxiomGT1.vcf')
    parser.add_argument('--export-txt-file',
            default='/BiOfs/BioProjects/AMORE-Axiom-20161123/apt-format-result-out/AxiomGT1.txt')
    parser.add_argument('--export-call-format', choices=('base_call'),
            default='base_call')
    args = parser.parse_args()
    main(args)

#/BiO/BioPeople/siyoo/Axiom/Tools/apt-1.19.0-x86_64-intel-linux/bin/apt-format-result \
#--calls-file /BiOfs/BioProjects/AMORE-Axiom-20161123/apt-genotype-axiom-out/AxiomGT1.calls.txt \
#--annotation-file /BiO/BioPeople/siyoo/Axiom/Libraries/Axiom_PMRA/Axiom_PMRA.na35.annot.db \
#--snp-identifier-column dbSNP_RS_ID \
#--snp-identifier-column probeset_id \
#--export-plink-file /BiOfs/BioProjects/AMORE-Axiom-20161123/apt-format-result-out/AxiomGT1.plink \
#--export-plinkt-file /BiOfs/BioProjects/AMORE-Axiom-20161123/apt-format-result-out/AxiomGT1.plinkt \
#--export-vcf-file /BiOfs/BioProjects/AMORE-Axiom-20161123/apt-format-result-out/AxiomGT1.vcf \
#--export-txt-file /BiOfs/BioProjects/AMORE-Axiom-20161123/apt-format-result-out/AxiomGT1.txt \
#--export-call-format base_call \
#--export-confidence \
#--export-log-ratio \
#--export-strength \
#--export-allele-signals
#--annotation-columns "Affy_SNP_ID,dbSNP_RS_ID,dbSNP_Loctype,Chromosome,Physical_Position,Position_End,Strand,Allele_A,Allele_B,Ref_Allele,Alt_Allele,Associated_Gene"
