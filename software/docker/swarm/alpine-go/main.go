package main

import (
	"flag"
	"fmt"
	"net/http"
	"os"
)

var (
	host, port string
)

func main() {
	flag.StringVar(&host, "host", "", "host usage")
	flag.StringVar(&port, "port", ":9090", "host usage")
	flag.Parse()

	name, _ := os.Hostname()
	fmt.Println(host, port, name)

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Hostname=%s, uri=%s!", name, r.URL.Path[1:])
	})

	panic(http.ListenAndServe(port, nil))
}
