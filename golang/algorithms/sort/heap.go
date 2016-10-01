package sort

import "fmt"

func HeapSort(slice []int) {
	n := len(slice)
	buildMaxHeap(slice, n)
	fmt.Println(slice)

	heapSize := n
	for i := n - 1; i > 0; i-- {
		swap(slice, 0, i)
		heapSize--
		maxHeapify(slice, 0, heapSize)
	}
}

func maxHeapify(slice []int, curIndex, heapSize int) {
	left := curIndex*2 + 1
	right := curIndex*2 + 2
	biggest := curIndex

	if left < heapSize && slice[left] > slice[biggest] {
		biggest = left
	}

	if right < heapSize && slice[right] > slice[biggest] {
		biggest = right
	}

	if biggest != curIndex {
		swap(slice, biggest, curIndex)
		// why inside the condition?
		maxHeapify(slice, biggest, heapSize)
	}

}

func buildMaxHeap(slice []int, heapSize int) {
	parentIndex := (len(slice) - 2) / 2
	for i := parentIndex; i >= 0; i = i - 1 {
		maxHeapify(slice, i, heapSize)
	}
}
