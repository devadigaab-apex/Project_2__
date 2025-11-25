import sys
#usage: cat fasta_fikle.fasta | python multi_line_fasta.py > output_file
c=0
for i in sys.stdin:
    if i.startswith(">"):
        c+=1
        if c>1:
            print("")
            print(i.strip())
        else:
            print(i.strip())
    else:
        print(i.strip(),end="")

