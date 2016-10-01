package linkedList

import "fmt"

type node struct {
	data int
	next *node
}

func newNode(data int) *node {
	return &node{data, nil}
}

var head *node

func createList(n int) {
	i := 1
	var tmp *node
	for i <= n {
		node := newNode(i)
		if head == nil {
			head = node
			tmp = head
		} else {
			tmp.next = node
			tmp = node
		}
		i++
	}
}

func printList() {
	current := head
	for current != nil {
		fmt.Printf("%d ", current.data)
		current = current.next
	}
	fmt.Println("")
}
