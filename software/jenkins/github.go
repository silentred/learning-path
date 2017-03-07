package main

import (
	"fmt"
	"time"

	"github.com/phayes/hookserve/hookserve"
)

func main() {
	server := hookserve.NewServer()
	server.Port = 8888
	server.Secret = "supersecretcode"
	server.GoListenAndServe()

	for {
		select {
		case event := <-server.Events:
			fmt.Println(event.Owner + " " + event.Repo + " " + event.Branch + " " + event.Commit)
		default:
			time.Sleep(100)
		}
	}
}
