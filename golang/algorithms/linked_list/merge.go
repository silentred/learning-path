package linkedList

import "fmt"

type linkedList struct {
	head *node
}

func (list *linkedList) mergeList(listB *linkedList) {
	if listB == nil || listB.head == nil {
		return
	}

	if list.head == nil {
		list.head = listB.head
		return
	}

	var aPrev *node
	//var bPrev *node
	aCurr := list.head
	bCurr := listB.head

	for aCurr != nil && bCurr != nil {

		aNext := aCurr.next
		bNext := bCurr.next

		fmt.Println(aCurr, bCurr, aPrev, aNext, bNext)
		if aCurr.data <= bCurr.data {
			// aCurr.next = bCurr
			// bCurr.next = aNext

			// move on
			aPrev = aCurr
			aCurr = aNext
		} else {
			if aPrev == nil {
				list.head = bCurr
			} else {
				aPrev.next = bCurr
			}
			bCurr.next = aCurr

			// move on
			aPrev = bCurr
			bCurr = bNext
		}
	}

	fmt.Println(aPrev, aCurr, bCurr)
	if bCurr != nil {
		aPrev.next = bCurr
	}

}

func newLinkedList(start, n int) *linkedList {
	ret := new(linkedList)

	i := start
	var tmp *node
	for i <= n {
		node := newNode(i)
		if ret.head == nil {
			ret.head = node
			tmp = ret.head
		} else {
			tmp.next = node
			tmp = node
		}
		i++
	}

	return ret
}

func printLinkedList(list *linkedList) {
	current := list.head
	for current != nil {
		fmt.Printf("%d ", current.data)
		current = current.next
	}
	fmt.Println("")
}
