package array

func rearrangeNaive(slice []int) []int {
	var posBuf []int
	var negBuf []int

	n := len(slice)
	setIndex := 0
	for i := 0; i < n; i++ {
		if slice[i] >= 0 {
			posBuf = append(posBuf, slice[i])
		} else {
			negBuf = append(negBuf, slice[i])
		}

		// even index
		if setIndex%2 == 0 {
			if len(posBuf) > 0 {
				slice[setIndex], posBuf = shift(posBuf)
				setIndex++
			}
			continue
		} else {
			if len(negBuf) > 0 {
				slice[setIndex], negBuf = shift(negBuf)
				setIndex++
			}
			continue
		}
	}

	// if there is more left in buffer

	for setIndex <= n-1 {
		if setIndex%2 == 0 {
			if len(posBuf) > 0 {
				slice[setIndex], posBuf = shift(posBuf)
				setIndex++
				continue
			}
		} else {
			if len(negBuf) > 0 {
				slice[setIndex], negBuf = shift(negBuf)
				setIndex++
				continue
			}
		}

		if len(posBuf) > 0 {
			slice[setIndex], posBuf = shift(posBuf)
			setIndex++
			continue
		}

		if len(negBuf) > 0 {
			slice[setIndex], negBuf = shift(negBuf)
			setIndex++
			continue
		}
	}

	return slice
}

func shift(slice []int) (int, []int) {
	return slice[0], slice[1:]
}

func reArrange(slice []int) {
	for i := 0; i < len(slice); i++ {
		if !atRightPosition(slice, i) {
			nextOppositeIndex := getNextOpposite(slice, i)
			if nextOppositeIndex != -1 {
				moveTailToHead(slice, i, nextOppositeIndex)
			} else {
				break
			}
		}
	}
}

func getNextOpposite(slice []int, index int) int {
	for i := index + 1; i < len(slice); i++ {
		if slice[i]*slice[index] < 0 {
			return i
		}
	}

	return -1
}

func moveTailToHead(slice []int, low, high int) {
	last := slice[high]
	for i := high; i > low; i-- {
		slice[i] = slice[i-1]
	}

	slice[low] = last
}

func atRightPosition(slice []int, i int) bool {
	if i%2 == 0 {
		if slice[i] > 0 {
			return true
		}
		return false
	} else {
		if slice[i] > 0 {
			return false
		}
		return true
	}
}
