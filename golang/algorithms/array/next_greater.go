package array

import "fmt"

//98, 23, 54, 12, 20, 7, 27
func nextGreater(slice []int) {
	n := len(slice)
	stack := make(Stack, 0)
	stack = stack.Push(slice[0])

	for i := 1; i < n; i++ {
		for !stack.IsEmpty() && slice[i] > stack.Peek() {
			fmt.Printf("num %d - next greater %d \n", stack.Peek(), slice[i])
			stack, _ = stack.Pop()
		}
		stack = stack.Push(slice[i])
	}

	var orphon int
	for !stack.IsEmpty() {
		stack, orphon = stack.Pop()
		fmt.Printf("num %d - next greater nil \n", orphon)
	}
}

type Stack []int

func (s Stack) Push(v int) Stack {
	return append(s, v)
}

func (s Stack) Pop() (Stack, int) {
	// FIXME: What do we do if the stack is empty, though?
	l := len(s)
	if l == 0 {
		return s, 0
	}

	return s[:l-1], s[l-1]
}

func (s Stack) IsEmpty() bool {
	return len(s) == 0
}

func (s Stack) Peek() int {
	// if s is empty, panic
	if s.IsEmpty() {
		panic("empty stack, cannot peek")
	}
	return s[len(s)-1]
}
