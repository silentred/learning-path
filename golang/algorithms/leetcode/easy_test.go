package leetcode

import (
	"fmt"
	"testing"
)

func TestRev(t *testing.T) {
	fmt.Println(reverse(1))
}

func TestAtoi(t *testing.T) {
	// start with 0;
	// minus
	fmt.Println(myAtoi("123"))
	fmt.Println(myAtoi("-123"))
	fmt.Println(myAtoi("-"))
	fmt.Println(myAtoi("   010"))
	fmt.Println(myAtoi("+-2"))
	fmt.Println(myAtoi("  +2ab23"))
	fmt.Println(myAtoi("   + 123"))
	fmt.Println(myAtoi("2147483648"))
	fmt.Println(myAtoi("-9223372036854775809"))
}

func TestPalindrome(t *testing.T) {
	fmt.Println(isPalindrome(12321))
	romanToInt("VIII")
}

func TestRoman(t *testing.T) {
	fmt.Println(romanToInt("VIII"))
	fmt.Println(romanToInt("XCII"))
	fmt.Println(romanToInt("XLVIII"))
}

func TestPrefix(t *testing.T) {
	fmt.Println(longestCommonPrefix([]string{"123", "125555"}))
	fmt.Println(longestCommonPrefix([]string{"a"}))
	fmt.Println(longestCommonPrefix([]string{"aa", "aa"}))
}

func TestReverseList(t *testing.T) {
	head := createList(5)
	head = reverseList(head)
	printList(head)
}

func createList(n int) *ListNode {
	head := &ListNode{Val: 1}
	var curr *ListNode = head
	for i := 2; i < n; i++ {
		curr.Next = &ListNode{Val: i}
		curr = curr.Next
	}

	return head
}

func printList(head *ListNode) {
	current := head
	for current != nil {
		fmt.Printf("%d ", current.Val)
		current = current.Next
	}
	fmt.Println("")
}
