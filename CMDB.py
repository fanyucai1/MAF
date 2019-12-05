import requests
import demjson
import os
from pathos.pools import ProcessPool
#################################################as follows you want to input
yourbed=''
yourkey=''
################################################
if not os.path.exists("CMDB.tsv"):
    outfile = open("CMDB.tsv", "w")
    outfile.write("#Chr\tPos\tID\tRef\tAlt\tallele_count\tallele_freq\n")
    outfile.close()
def run(chr,pos):
    html = 'http://db.cngb.org/cmdb/api/v1.0/variant?type=position&query=%s-%s&token=%s'%(chr,pos,yourkey)
    try:
        res = requests.get(html)
        ret = demjson.decode(res.text)
        print(ret)
        outfile = open("CMDB.tsv", "a+")
        for entry in ret:
            if not 'code' in entry:
                outfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(entry['chrom'],entry['pos'],entry['rsid'],entry['ref'],entry['alt'],entry['allele_count'],entry['allele_freq']))
        outfile.close()
    except:
        pass
if __name__=="__main__":

    infile = open(yourbed, "r")
    infile2=open("CMDB.tsv", "r")
    site={}
    for line in infile2:
        if not line.startswith("#"):
            line=line.strip()
            array=line.split("\t")
            site[array[0]]=1
    infile2.close()
    for line in infile:
        if not line.startswith("#"):
            line = line.strip()
            array = line.split("\t")
            pos = []
            chr = []
            for i in range(int(array[1]), int(array[2]) + 1):
                if i not in site:
                    pos.append(i)
                    chr.append(array[0])
            pool = ProcessPool(nodes=3)
            pool.map(run, chr, pos)
