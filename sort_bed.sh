#!/bin/bash

INPUT_FILE="$1"           
OUTPUT_FILE="sorted_query.bed.gz"


zcat "$INPUT_FILE" |sort -k1,1V -k2,2n  | gzip > "$OUTPUT_FILE"

echo "Sorted file created $OUTPUT_FILE"
