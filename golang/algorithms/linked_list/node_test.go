package linkedList

import "testing"

func TestNodeCreate(t *testing.T) {
	createList(10)
	printList()
}

func TestReverse(t *testing.T) {
	createList(10)
	reverseList()
	printList()
	reverseRecursive(head)
	printList()
}
