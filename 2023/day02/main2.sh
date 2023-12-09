#!/usr/bin/bash


# Part 2
INPUT_FILE="input.txt"

while read -r line ; do
  cleaned_line=$(echo "$line" | cut -d':' -f2 | sed 's/^ //g')
  fewest_reds=$(grep -o "[0-9]\+\sred\+" <<< "$cleaned_line" | awk '{print $1}' | sort -rn | head -n1)
  fewest_blues=$(grep -o "[0-9]\+\sblue\+" <<< "$cleaned_line" | awk '{print $1}' | sort -rn | head -n1)
  fewest_greens=$(grep -o "[0-9]\+\sgreen\+" <<< "$cleaned_line" | awk '{print $1}' | sort -rn | head -n1)
  printf "(%s)\n" "$fewest_reds * $fewest_blues * $fewest_greens"
done < "$INPUT_FILE" \
  | paste -sd+ \
  | bc
