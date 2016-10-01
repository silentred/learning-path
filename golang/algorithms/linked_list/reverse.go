package linkedList

func reverseList() {
	next := head
	var current *node
	var prev *node
	for next != nil {
		current = next
		next = next.next
		current.next = prev
		prev = current
	}

	head = current
}

func reverseRecursive(curr *node) {
	if curr == nil {
		return
	}

	if curr.next == nil {
		head = curr
		return
	}

	reverseRecursive(curr.next)
	curr.next.next = curr
	curr.next = nil
}
