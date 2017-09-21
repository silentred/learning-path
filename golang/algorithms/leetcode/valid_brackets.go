package leetcode

// {([{}[]])}
func isValid(s string) bool {
	if len(s)%2 > 0 {
		return false
	}

	var leftParts = []byte{'[', '{', '('}
	var index = map[byte]int{
		']': '[' * -1,
		'}': '{' * -1,
		')': '(' * -1,
	}

	var stack = make([]byte, 0, len(s)/2)

	for _, b := range []byte(s) {
		if inSliceByte(leftParts, b) {
			stack = append(stack, b)
		} else {
			if len(stack) > 0 && int(stack[len(stack)-1])+index[b] == 0 {
				//pop
				stack = stack[:len(stack)-1]
			} else {
				return false
			}
		}
	}

	return len(stack) == 0
}

func inSliceByte(s []byte, b byte) bool {
	for _, item := range s {
		if b == item {
			return true
		}
	}
	return false
}
