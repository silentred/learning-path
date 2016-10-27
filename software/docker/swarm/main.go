package main

import (
	"flag"
	"fmt"
	"net/http"
)

var (
	host, port string
)

func main() {
	flag.StringVar(&host, "host", "", "host usage")
	flag.StringVar(&port, "port", "9090", "host usage")
	flag.Parse()

	fmt.Println(host, port)

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Hi there, I love %s!", r.URL.Path[1:])
	})

	panic(http.ListenAndServe(":9090", nil))
}
