package main

import (
	"fmt"
	"os"
	"strings"
)

func main() {
	b, _ := os.ReadFile("input.txt")
	data := strings.Split(string(b), "\n")
	n := len(data)
	fmt.Println(n)
	for i, line := range data {
		fmt.Println(i, line)
	}
}
