import re
import glob
import csv
from tqdm import tqdm


class CSV_PARSER():
    # Category 1: Provided Methods
    def __init__(self, pth):
        self.pth = pth+'/'
        self.main()
    def load_files(self, path):
        # make a list of all pdf files in given path
        return glob.glob(path + "/*.tsv")
    
    def GET_DATA(self, path):
        rows = []
        with open(path) as fd:
            rd = csv.reader(fd, delimiter="\t", quotechar='"')
            for row in rd:
                if row != []:
                    rows.append(row)   
        srt = [e for e, row in enumerate(rows) if row[0] == 'Merchant SKU']
        LST = []
        Shipment_Data = ' '
        ship_id = ''
        date = ''
        FC_state = ''
        Cost = ' '
        MSKU = []
        ASIN = []
        QTY  = []
        for e, row in enumerate(rows):
            if row[0] == 'Shipment ID':
                ship_id = row[-1]
            if row[0] == 'Name':
                try:
                    row1 = row[1].replace('/', '-')
                    res = re.search("(\d{2}[-]+\d{2}[-]+\d{4})", row1)
                    date = res[0]
                except:
                    date = ''
            if row[0] == 'Ship To':
                FC_state = row[-1]
            if e > srt[0]:
                MSKU.append(row[0]) 
                ASIN.append(row[2])
                if row[-1].isnumeric() == True:
                    QTY.append(row[-1])
        for i in range(len(MSKU)):
            lst = [Shipment_Data, ship_id, FC_state, date, Cost, MSKU[i], ASIN[i], QTY[i]]
            LST.append(lst)
        return LST
    
    def main(self):
        hdr = ['Shipment-Data', 'Shipment-ID', 'FC-State', 'Date', 'Cost', 'MSKU', 'ASIN', 'Qty']
        path = self.pth
        files = self.load_files(path)
        with open('Output.csv', 'w', newline = '') as output_csv:
            # initialize rows writer
            csv_writer = csv.writer(output_csv)
            # write headers to the file
            csv_writer.writerow(hdr)
            c = 0
            for file in tqdm(files):
                try:
                    lst = self.GET_DATA(file)
                    if lst != []:
                        for l in lst:
                            csv_writer.writerow(l)
                    c+=1
                    print(c, 'File Processed...')
                except:
                    pass
        print('\n\n','Process Completed')
        return
