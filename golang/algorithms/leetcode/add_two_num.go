package leetcode

type ListNode struct {
	Val  int
	Next *ListNode
}

func addTwoNumbers(l1 *ListNode, l2 *ListNode) *ListNode {
	var result *ListNode
	var plus bool

	result = nil

	for l1 != nil || l2 != nil {
		var left, right int
		if l1 != nil {
			left = l1.Val
			l1 = l1.Next
		}

		if l2 != nil {
			right = l2.Val
			l2 = l2.Next
		}

		val := left + right
		if plus {
			val++
		}

		if val >= 10 {
			val = val - 10
			plus = true
		} else {
			plus = false
		}

		if result == nil {
			result = &ListNode{Val: val}
		} else {
			var node *ListNode
			node = result
			for node.Next != nil {
				node = node.Next
			}
			node.Next = &ListNode{Val: val}
		}
	}

	if plus {
		var node *ListNode
		node = result
		for node.Next != nil {
			node = node.Next
		}
		node.Next = &ListNode{Val: 1}
	}

	return result

}
