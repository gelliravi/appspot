#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Convert the proofed data from maggie into the tables defined in
athalina/models.py (for http://biocon.berkeley.edu/athaliana)
'''

import sys
import csv
import re
import string


def strip_non_printable(s):
    return ''.join(x for x in s if x in string.printable).strip()


def get_gene(gene):
    if len(gene) > 1 and (gene[:2] not in ('FN', 'FB')): return gene
    return '-'


def get_code(*args):
    for a in args:
        if len(a) > 1 and (a[:2] not in ('FN', 'FB')): return 'S'

    a = sorted(args, key=lambda x: ('SFG-'.index(x[0]), x))
    code = re.sub("\d+", "", a[0])
    return code 


def read_gene_families():
    fn = "gene_families"
    print >>sys.stderr, "read", fn
    fp = open(fn)
    reader = csv.reader(fp, delimiter='\t')
    reader.next()
    families = {}
    for row in reader:
        family, gene = row
        family = strip_non_printable(family)
        gene = strip_non_printable(gene).split('.')[0].upper()
        families[gene] = family

    return families


def main():
    fp = open("FINAL master positional history spreadsheet.txt")
    reader = csv.reader(fp, delimiter='\t')
    fw = open("data.csv", "w")
    writer = csv.writer(fw)
    header = "athaliana,type,description,gene_family,"+\
             "lyrata1,papaya1,poplar1,poplar2,grape1," +\
             "lyrata_code,papaya_code,poplar_code,grape_code,gevo_link"
    header = header.split(',')
    families = read_gene_families()
    writer.writerow(header)
    reader.next()
    for rownum, row in enumerate(reader):
        for i, r in enumerate(row):
            if r.strip() in ('', '.'):
                row[i] = '-'
            else:
                row[i] = r.strip()
        # add four columns with the code designation in
        # TODO: this is now hard-coded
        athaliana_props = row[:3]
        athaliana = athaliana_props[0]
        athaliana_family = families.get(athaliana, '-')
        athaliana_props.append(athaliana_family)

        genes = row[3:-1]
        #print genes
        gevo_link = row[-1]
        new_genes = [get_gene(x) for x in genes]
        lyrata1, papaya1, poplar1, poplar2, grape1 = genes
        lyrata_code = get_code(lyrata1) 
        papaya_code = get_code(papaya1) 
        poplar_code = get_code(poplar1, poplar2) 
        grape_code = get_code(grape1) 
        codes = [lyrata_code, papaya_code, poplar_code, grape_code]
        #print codes 
        row = athaliana_props + new_genes + codes + [gevo_link]
        writer.writerow(row)
        #raw_input()

    print >>sys.stderr, "total %d rows converted" % rownum


if __name__ == '__main__':
    main()
