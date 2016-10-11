package array

func longestNonRepeatingSubstr(str string) string {
	charIndex := make([]int, 256)
	initCharIndex(charIndex)

	var startIdx int
	var currLength int = 1
	var maxLength int = 1
	var prevIdx int
	var char byte

	for i := 1; i < len(str); i++ {
		char = str[i]

		prevIdx = charIndex[char]

		if prevIdx == -1 || i-currLength > prevIdx {
			currLength++
		} else {
			if currLength > maxLength {
				maxLength = currLength
				startIdx = i - maxLength
			}
			currLength = i - prevIdx
		}

		charIndex[char] = i

	}

	if currLength > maxLength {
		maxLength = currLength
		startIdx = len(str) - maxLength
	}

	return str[startIdx : startIdx+maxLength]
}

func initCharIndex(charIndex []int) {
	for i := 0; i < len(charIndex); i++ {
		charIndex[i] = -1
	}
}
