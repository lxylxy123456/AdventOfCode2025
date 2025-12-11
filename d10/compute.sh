#!/bin/bash
set -xeo pipefail

TMPD="$(mktemp -d)"
grep '^Your puzzle answer was' q.txt | cut -d ' ' -f 5- \
	| grep -oE '[0-9a-z,]+' > "$TMPD/expected"
diff <(wc -l < "$TMPD/expected") <(echo 2)

make -j 2

time python3 s.py in.txt --test-scratch | tee -a "$TMPD/actual"
time python3 s1.py in.txt | tee -a "$TMPD/actual"

while read EXPECTED; do
	grep -w "$EXPECTED" "$TMPD/actual"
done < "$TMPD/expected"

rm -r "$TMPD"

