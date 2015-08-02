package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

func handlerA(w http.ResponseWriter, r *http.Request) {
	io.WriteString(w, "Hello world!")
}

func handlerB(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")

	myItems := []string{"item1", "item2", "item3"}
	a, _ := json.Marshal(myItems)

	fmt.Println("hello")

	w.Write(a)
	return
}

func main() {
	http.HandleFunc("/", handlerB)
	http.ListenAndServe(":8080", nil)
}
