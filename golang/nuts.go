package main

import (
	"fmt"
	"time"
)

func main() {
	Me := &Programmer{100, 0}
	TheOne := make(chan Girl)

	go func() {
		for {
			girl := Me.waitingFor(TheOne)
			girl.givesGoodManCardTo(Me)
			Me.healingSelf()
		}
	}()

	for {
		girl := Girl{}
		TheOne <- girl
	}
}

type Programmer struct {
	Health           int
	GoodManCardCount int
}

func (person *Programmer) healingSelf() {
	time.Sleep(time.Second * 1)
	person.Health = 100
	fmt.Println(fmt.Sprintf("Card Count is %d", person.GoodManCardCount))
}

func (person *Programmer) waitingFor(theOne chan Girl) Girl {
	girl := <-theOne
	return girl
}

type Girl struct {
}

func (girl *Girl) givesGoodManCardTo(person *Programmer) {
	person.Health -= 99
	person.GoodManCardCount++
}
