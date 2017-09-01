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
	totalSize   = 500 << 20 // 500MB
	filePath    = "/tmp/data"
	imgFilePath = "/tmp/output.dat"
	content     = strings.Repeat("a", pageSize)
)

func main() {
	flag.IntVar(&totalSize, "size", totalSize, "total size to write")
	flag.Parse()

	duration := write(filePath, os.O_CREATE|os.O_APPEND|os.O_WRONLY, totalSize)
	fmt.Printf("Write %d bytes to wr-layer, cost %s \n", totalSize, duration)

	duration = read(filePath, totalSize)
	fmt.Printf("Read %d bytes from wr-layer, cost %s \n", totalSize, duration)

	duration = append(imgFilePath, 5)
	fmt.Printf("[Img] Append %d times, cost %s \n", 5, duration)
	duration = read(imgFilePath, 100<<20)
	fmt.Printf("[Img] Read %d bytes from image-layer, cost %s \n", 100<<20, duration)
}

func write(fileName string, flag, total int) time.Duration {
	file, err := os.OpenFile(fileName, flag, 0600)
	defer file.Close()

	if err != nil {
		log.Fatalln(err)
	}
	var bytesWriten int
	var timeStart = time.Now()
	for bytesWriten < total {
		n, err := file.WriteString(content)
		if err != nil {
			log.Printf("write error: %v \n", err)
			break
		}
		bytesWriten += n
	}
	duration := time.Now().Sub(timeStart)
	return duration
}

func read(fileName string, total int) time.Duration {
	var buf = make([]byte, pageSize)
	file, err := os.Open(fileName)
	if err != nil {
		log.Fatalln(err)
	}
	var bytesRead int
	timeStart := time.Now()
	for bytesRead < total {
		n, err := file.Read(buf)
		if err != nil {
			log.Printf("read error: %v \n", err)
			break
		}
		bytesRead += n
	}
	duration := time.Now().Sub(timeStart)
	file.Close()
	return duration
}

func append(fileName string, cnt int) time.Duration {
	// append to file
	timeStart := time.Now()
	file, err := os.OpenFile(imgFilePath, os.O_APPEND|os.O_WRONLY, 0600)
	if err != nil {
		log.Fatalln(err)
	}
	for i := 0; i < cnt; i++ {
		_, err = file.WriteString(content)
		if err != nil {
			log.Fatalf("append error: %v", err)
		}
	}
	duration := time.Now().Sub(timeStart)
	file.Close()
	return duration
}
