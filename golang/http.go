package main

import (
	"encoding/json"
	"io"
	"net/http"
)

func handlerA(w http.ResponseWriter, r *http.Request) {
	io.WriteString(w, "Hello world!")
}

func handlerB(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")

	myItems := []string{"item1", r.RemoteAddr}
	a, _ := json.Marshal(myItems)

	w.Write(a)
	return
}

func main() {
	http.HandleFunc("/", handlerB)
	http.ListenAndServe("127.0.0.1:8080", nil)
}
