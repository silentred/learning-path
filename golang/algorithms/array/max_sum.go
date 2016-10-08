package array

func maxSum(slice []int) int {
	if len(slice) == 0 {
		return 0
	}

	var maxSum int
	var curSum int

	var allNegative = true
	var maxNegative int

	for i := 0; i < len(slice); i++ {
		if maxNegative == 0 && slice[i] < 0 {
			maxNegative = slice[i]
		}

		if allNegative && slice[i] > 0 {
			allNegative = false
		} else if allNegative && slice[i] < 0 && maxNegative < slice[i] {
			maxNegative = slice[i]
		}

		curSum += slice[i]
		if curSum < 0 {
			curSum = 0
		}

		if maxSum < curSum {
			maxSum = curSum
		}
	}

	if allNegative {
		maxSum = maxNegative
	}

	return maxSum
}
