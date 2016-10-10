package array

func rotate(slice []int, k int) {
	n := len(slice)
	reverse(slice, 0, k-1)
	reverse(slice, k, n-1)
	reverse(slice, 0, n-1)
}

func reverse(slice []int, start, end int) {
	for start < end {
		slice[start], slice[end] = slice[end], slice[start]
		start++
		end--
	}
}
