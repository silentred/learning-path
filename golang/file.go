package main

import (
	"net/http"
	"os"
)

func main() {
	argsWithProg := os.Args
	dirName := argsWithProg[1]

	file, err := os.Open(dirName)
	if err != nil {
		panic(err)
	}

	stat, err := file.Stat()
	if err != nil {
		panic(err)
	}

	if stat.IsDir() {
		fs := http.FileServer(http.Dir(dirName))
		http.Handle("/", fs)
		http.ListenAndServe(":8081", nil)
	}

	panic(dirName)
}