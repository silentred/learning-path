package array

import "fmt"

func firstNonRepeating(str string) {
	count := make([]int, 256)
	n := len(str)

	for i := 0; i < n; i++ {
		count[str[i]]++
	}

	for j := 0; j < n; j++ {
		if count[str[j]] == 1 {
			fmt.Println("first char is ", string(str[j]))
			return
		}
	}
}

func firstNonRepeatingOptimized(str string) {
	l := 256
	index := make([]int, l)
	n := len(str)

	// init to -1
	for i := 0; i < l; i++ {
		index[i] = -1
	}

	for i := 0; i < n; i++ {
		// if first appeared, set current position to value
		if index[str[i]] == -1 {
			index[str[i]] = i
		} else {
			// if repeat, set to -2
			index[str[i]] = -2
		}
	}

	minIndex := n
	for i := 0; i < l; i++ {
		// index[i] > 0 meaning no repeating
		if index[i] > 0 && minIndex > index[i] {
			minIndex = index[i]
		}
	}

	fmt.Println(minIndex, string(str[minIndex]))

}
