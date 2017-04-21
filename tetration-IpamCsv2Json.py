"""
tetration-IpamCsv2Json takes the CSV output from an IPAM and
converts it to JSON format for consumption by Cisco Tetration
as Side Information about your network for an ADM run.

The CSV file ***must***
1) Have a header row, although the actual headers don't matter
2) The first two columns must contain the subnet (first column)
   and the name or description of the subnet (second column).
   Any additional columns will be ignored, so they don't matter.

The JSON output file will be in the format:
{
    "configs": [
        {
            "subnet": "10.46.0.0/24",
            "name": "subnet name or desc"
        },
        {
            "subnet": "10.46.1.0/24",
            "name": "subnet name or desc"
        }
    ]
}

written by Doron Chosnek, April 2017
"""

import json
import sys

if len(sys.argv) <> 2:
    print "\nPlease specify a CSV file for input\n"
    print sys.argv[0] + " filename.csv\n"
    quit()

fname_csv = sys.argv[1]
fname_json = fname_csv.replace('.csv', '.json')

js = {"configs": []}

# each row in the CSV file will be it's own dictionary:
# d = {"subnet": "10.46.0.0/24", "name": "subnet name"}
# and that dict will be appended to js["configs"]
# Finally, js will be dumped to a JSON file.
with open(fname_csv) as f:
    f.readline()    # discard header row
    for line in f.readlines():
        # split each row of the CSV file and remove double quotes
        d = {}
        parts = line.split(',')
        d["subnet"] = str(parts[0]).replace('"', '')
        d["name"] = str(parts[1]).replace('"', '')
        js["configs"].append(d)

with open(fname_json, 'w') as outfile:
    print "Writing " + fname_json
    json.dump(js, outfile, indent=2)
