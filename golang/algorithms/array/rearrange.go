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
