#!/usr/bin/bash


# Part 1
INPUT_FILE="input.txt"

while read -r line ; do
  cleaned_line=$(echo "${line//[a-z]/}" | fold -w1)
  first_number=$(printf '%s' "$cleaned_line" | head -n1)
  last_number=$(printf '%s' "$cleaned_line" | tail -n1)
  printf "%s%s\n" "$first_number" "$last_number"
done < "$INPUT_FILE" \
| paste -sd+ \
| bc
