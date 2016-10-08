package array

func bSearch(slice []int, target int) int {
	if len(slice) == 0 {
		return -1
	}

	right := len(slice) - 1
	left := 0

	for left <= right {
		mid := (left + right) / 2

		if slice[mid] > target {
			right = mid - 1
		} else if slice[mid] < target {
			left = mid + 1
		} else {
			return mid
		}
	}

	return -1
}
