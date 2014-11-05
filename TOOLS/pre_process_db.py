import csv
import sys

"""

"""

def main():
    f=sys.argv[-2]
    fout=sys.argv[-1]
    output = csv.writer(open(fout, 'w'), delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #    output=open('processed_db.txt','w')
    with open(f, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            output.writerow([row[i] for i in [0,1,2,8,11,24,18,12,13,23,14]])
if __name__=="__main__":
   main()
