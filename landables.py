import argparse
import csv
import sys

def parse_latlon(str):
    if str[-1] in "NS":
        deg = int(str[:2])
        min = float(str[2:-1])
        sign = 1 if str[-1] == "N" else -1
    else:
        deg = int(str[:3])
        min = float(str[3:-1])
        sign = 1 if str[-1] == "E" else -1

    return sign * (deg + min / 60)

def parse_outlandings(outlandings_file):
    reader = csv.DictReader(outlandings_file)

    out = []
    for row in reader:
        if len(row['code']) != 4 or row['code'][-1] not in "ASM":
            # Only air fields, air strips and military fields
            continue

        lat = parse_latlon(row['lat'])
        lon = parse_latlon(row['lon'])
        if lat > 54:
            # Southern England only
            continue

        out.append(row)

    return out

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("outlandings_file", nargs="?",
                         help="List of outlandins file",
                         type=argparse.FileType("r"), default=sys.stdin)
    parser.add_argument("out_file", nargs="?",
                         help="Output file",
                         type=argparse.FileType("wt"), default=sys.stdout)

    args = parser.parse_args()

    outlandings = parse_outlandings(args.outlandings_file)

    fieldnames = outlandings[0].keys()
    writer = csv.DictWriter(args.out_file, fieldnames)
    writer.writeheader()
    for outlanding in outlandings:
        writer.writerow(outlanding)
