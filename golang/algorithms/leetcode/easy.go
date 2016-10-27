package leetcode

import "fmt"

func reverse(x int) int {
	digits := make([]int, 0)
	var mod int
	for x > 0 {
		mod = x % 10
		digits = append(digits, mod)
		x = x / 10
	}

	var result int
	n := len(digits)
	for i := 0; i < n; i++ {
		p := n - i - 1
		result += digits[i] * pow10(p)
	}

	var max, min int
	max = 1<<31 - 1
	min = (1 << 31) * -1

	fmt.Println(max, min, result)
	if result > max || result < min {
		result = 0
	}

	return result
}

func pow10(n int) int {
	m := 1
	for j := 0; j < n; j++ {
		m *= 10
	}
	return m
}

func myAtoi(str string) int {
	var result int
	var zero byte = '0'
	var nine byte = '9'
	var minus bool
	var hasSign bool
	var validDigits []int
	var startCounting bool

	n := len(str)
	if n == 0 {
		return result
	}

	var tmpNum int
	var tmp byte
	for i := 0; i < n; i++ {
		tmp = str[i]
		// if invalid
		if tmp < zero || tmp > nine {
			if startCounting {
				break
			}

			if isEmptyChar(tmp) {
				continue
			}

			if tmp == '+' && !hasSign {
				hasSign = true
				startCounting = true
				continue
			} else if tmp == '-' && !hasSign {
				hasSign = true
				minus = true
				startCounting = true
				continue
			}

			break
		}

		startCounting = true
		tmpNum = int(tmp - zero)
		//result += tmpNum * pow10(n-1-i)
		validDigits = append(validDigits, tmpNum)
	}

	var overflow bool
	for i, val := range validDigits {
		result += val * pow10(len(validDigits)-1-i)
		if result < 0 {
			overflow = true
		}
	}

	if minus {
		result *= -1
	}

	var max, min int
	max = 1<<31 - 1
	min = (1 << 31) * -1

	if overflow && !minus {
		return max
	} else if overflow && minus {
		return min
	}

	if result > max {
		result = max
	} else if result < min {
		result = min
	}

	return result
}

func isEmptyChar(b byte) bool {
	empty := []byte{' ', '\t', '\n', '\r'}
	for _, k := range empty {
		if b == k {
			return true
		}
	}
	return false
}

func isPalindrome(x int) bool {
	var digits []int
	var mod int
	for x > 0 {
		mod = x % 10
		digits = append(digits, mod)
		x = x / 10
	}

	var i int
	n := len(digits) - 1
	for i < n {
		if digits[i] != digits[n] {
			return false
		}
		i++
		n--
	}

	return true
}

func romanToInt(s string) int {
	n := len(s)
	nums := make([]int, n, n)
	var sum int
	var charMap = map[byte]int{
		'I': 1,
		'V': 5,
		'X': 10,
		'L': 50,
		'C': 100,
		'D': 500,
		'M': 1000,
	}

	for i := 0; i < n; i++ {
		char := s[i]
		nums[i] = charMap[char]
		if i > 0 && nums[i] > nums[i-1] {
			nums[i-1] *= -1
		}
	}

	for _, val := range nums {
		sum += val
	}

	return sum
}

func longestCommonPrefix(strs []string) string {
	if len(strs) == 0 {
		return ""
	}

	var result []byte
	var shortLen int
	shortLen = len(strs[0])
	for _, val := range strs {
		if shortLen > len(val) {
			shortLen = len(val)
		}
	}

	var tmp byte
	var leftLen = shortLen
	for leftLen > 0 {
		for i, str := range strs {
			if i == 0 {
				tmp = str[0]
			}
			if tmp != str[0] {
				return string(result)
			}
			strs[i] = str[1:]
		}
		result = append(result, tmp)
		leftLen--
	}

	return string(result)
}

type ListNode struct {
	Val  int
	Next *ListNode
}

func removeNthFromEnd(head *ListNode, n int) *ListNode {
	head = reverseList(head)
	var step int

	if n == 1 {
		head = head.Next
	} else {
		var prev, curr, next *ListNode
		next = head
		for next != nil && step < n {
			prev = curr
			curr = next

			next = curr.Next
			step++
		}
		prev.Next = next
	}

	return reverseList(head)
}

func reverseList(head *ListNode) *ListNode {
	var prev, curr, next *ListNode
	next = head
	for next != nil {
		curr = next
		next = next.Next
		curr.Next = prev
		prev = curr
	}

	return curr
}
