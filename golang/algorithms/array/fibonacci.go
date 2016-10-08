package array

func fib(n int) int {
	if n < 0 {
		return 0
	}

	if n == 0 || n == 1 {
		return n
	}

	var c int
	a := 0
	b := 1
	for i := 2; i <= n; i++ {
		c = a + b
		a = b
		b = c
	}

	return c
}
