# Takes the CSV output from an IPAM and
# converts it to JSON format for consumption by Cisco Tetration
# as Side Information about your network for an ADM run.

# The CSV file ***must***
# 1) Have a header row, although the actual headers don't matter
# 2) The first two columns must contain the subnet (first column)
#    and the name or description of the subnet (second column).
#    Any additional columns will be ignored, so they don't matter.

# The JSON output file will be in the format:
# {
#     "configs": [
#         {
#             "subnet": "10.46.0.0/24",
#             "name": "subnet name or desc"
#         },
#         {
#             "subnet": "10.46.1.0/24",
#             "name": "subnet name or desc"
#         }
#     ]
# }

# written by Doron Chosnek, April 2017

param (
    [Parameter(Mandatory=$true)][string]$Filename
)

# Build a hashtable where each line of the CSV becomes an entry under $js["configs"]
$js = @{}
$js["configs"] = Import-Csv $Filename -Header "subnet", "name" | Select-Object -Skip 1

# Export the hashtable to JSON. The encoding is very important to avoid hidden characters
# that would otherwise be injected at the beginning of the output file.
$js | ConvertTo-Json | Out-File -Encoding utf8 ($Filename -replace "\.csv", '.json')