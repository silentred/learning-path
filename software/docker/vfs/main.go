package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"strings"
	"time"
)

const (
	pageSize = 4 << 10 // 4k
)

var (
	totalSize = 1 << 30 // 1G
	filePath  = "/tmp/data"
	content   = strings.Repeat("a", pageSize)
)

func main() {
	flag.IntVar(&totalSize, "size", totalSize, "total size to write")
	flag.Parse()

	file, err := os.Create(filePath)
	if err != nil {
		log.Fatalln(err)
	}

	// write test
	var bytesWriten int
	var timeStart = time.Now()
	for bytesWriten < totalSize {
		n, err := file.WriteString(content)
		if err != nil {
			log.Printf("write error: %v \n", err)
		}
		bytesWriten += n
	}
	duration := time.Now().Sub(timeStart)
	file.Close()
	fmt.Printf("Write %d bytes, cost %s \n", totalSize, duration)

	// append to file
	timeStart = time.Now()
	file, err = os.OpenFile(filePath, os.O_APPEND|os.O_WRONLY, 0600)
	if err != nil {
		log.Fatalln(err)
	}
	for i := 0; i < 100; i++ {
		file.WriteString("test")
	}
	duration = time.Now().Sub(timeStart)
	file.Close()
	fmt.Printf("Append 100 times, cost %s \n", duration)

	// read test
	var buf = make([]byte, pageSize)
	file, err = os.Open(filePath)
	if err != nil {
		log.Fatalln(err)
	}
	var bytesRead int
	timeStart = time.Now()
	for bytesRead < totalSize {
		n, err := file.Read(buf)
		if err != nil {
			log.Printf("write error: %v \n", err)
		}
		bytesRead += n
	}
	duration = time.Now().Sub(timeStart)
	file.Close()
	fmt.Printf("Read %d bytes, cost %s \n", totalSize, duration)
}
