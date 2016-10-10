package array

func nextGreaterWithSameDigits(slice []int) {
	n := len(slice)

	var swichIndex int
	for i := n - 1; i > 0; i-- {
		if slice[i-1] < slice[i] {
			swichIndex = i - 1
			break
		}
	}

	var nextBiggerIndex int
	for i := n - 1; i > swichIndex; i-- {
		if nextBiggerIndex == 0 && slice[i] > slice[swichIndex] {
			nextBiggerIndex = i
		}

		if nextBiggerIndex > 0 && slice[i] < slice[nextBiggerIndex] {
			nextBiggerIndex = i
		}
	}

	slice[swichIndex], slice[nextBiggerIndex] = slice[nextBiggerIndex], slice[swichIndex]

	reverse(slice, swichIndex+1, n-1)
}

// func reverse(slice []int, low, high int) {
// 	for low < high {
// 		slice[low], slice[high] = slice[high], slice[low]
// 		low++
// 		high--
// 	}
// }
