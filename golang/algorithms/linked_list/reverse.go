package linkedList

func (list *linkedList) reverseList() {
	next := list.head
	var current *node
	var prev *node
	for next != nil {
		current = next
		next = next.next
		current.next = prev
		prev = current
	}

	list.head = current
}

func (list *linkedList) reverseRecursive(curr *node) {
	if curr == nil {
		return
	}

	if curr.next == nil {
		list.head = curr
		return
	}

	list.reverseRecursive(curr.next)
	curr.next.next = curr
	curr.next = nil
}
