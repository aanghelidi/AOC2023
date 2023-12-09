#!/usr/bin/bash


# Part 1
INPUT_FILE="input.txt"

impossible_games=$(while read -r line ; do
  game_id=$(grep -o '^Game [0-9]\+' <<< "$line" | awk '{print $2}')
  cleaned_line=$(echo "$line" | cut -d':' -f2 | sed 's/^ //g')
  c_reds=$(grep -o "[0-9]\+\sred\+" <<< "$cleaned_line" | awk '{print $1 ">12"}' | bc)
  c_greens=$(grep -o "[0-9]\+\sgreen\+" <<< "$cleaned_line" | awk '{print $1 ">13"}' | bc)
  c_blues=$(grep -o "[0-9]\+\sblue\+" <<< "$cleaned_line" | awk '{print $1 ">14"}' | bc)
  printf "%s\n" "$c_reds" | grep -q "1" && printf "%s\n" "$game_id"
  printf "%s\n" "$c_blues" | grep -q "1" && printf "%s\n" "$game_id"
  printf "%s\n" "$c_greens" | grep -q "1" && printf "%s\n" "$game_id"
done < "$INPUT_FILE")

cat $INPUT_FILE \
  | grep -o '^Game [0-9]\+' \
  | awk '{print $2}' \
  | grep -v "$impossible_games" \
  | paste -sd+ \
  | bc
