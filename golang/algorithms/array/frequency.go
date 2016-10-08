package array

// time O(n), space O(1)
func count(slice []int) []int {
	n := len(slice)
	for i := 0; i < n; i++ {
		slice[i]--
	}

	for j := 0; j < n; j++ {
		m := slice[j] % n
		slice[m] += n
	}

	res := make([]int, n)
	for k := 0; k < n; k++ {
		res[k] = slice[k] / n
	}

	return res
}
