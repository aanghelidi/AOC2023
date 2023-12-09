#!/usr/bin/bash


# Part 2
INPUT_FILE="input.txt"

while read -r line ; do
  cleaned_line=$(echo "$line" \
  | sed -e 's/one/one1one/g' \
  | sed -e 's/two/two2two/g' \
  | sed -e 's/three/three3three/g' \
  | sed -e 's/four/four4four/g' \
  | sed -e 's/five/five5five/g' \
  | sed -e 's/six/six6six/g' \
  | sed -e 's/seven/seven7seven/g' \
  | sed -e 's/eight/eight8eight/g' \
  | sed -e 's/nine/nine9nine/g' \
  | sed -e 's/[a-z]//g'\
  | sed -e 's/./&\n/g')
  first_number=$(printf '%s' "$cleaned_line" | head -n1)
  last_number=$(printf '%s' "$cleaned_line" | tail -n1)
  printf "%s%s\n" "$first_number" "$last_number"
done < "$INPUT_FILE" \
  | paste -sd+ \
  | bc
