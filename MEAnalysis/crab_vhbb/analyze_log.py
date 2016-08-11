import sys

n_xrootd = 0
for line in sys.stdin.readlines():
    line = line.lower().strip()
    if "tnetxngfile" in line and "error" in line:
        n_xrootd += 1

if n_xrootd>0:
    sys.exit(8028)
else:
    sys.exit(1)
