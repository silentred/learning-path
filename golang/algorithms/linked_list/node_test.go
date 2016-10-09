package linkedList

import "testing"

func TestNodeCreate(t *testing.T) {
	list := newLinkedList(1, 10)
	printLinkedList(list)
}

func TestReverse(t *testing.T) {
	list := newLinkedList(1, 10)
	list.reverseList()
	printLinkedList(list)
	list.reverseRecursive(list.head)
	printLinkedList(list)
}

func TestLinkedList(t *testing.T) {
	l := newLinkedList(1, 10)
	lb := newLinkedList(5, 15)
	l.mergeList(lb)
	printLinkedList(l)
}
