package main

import (
    "fmt"
)

func main() {
    var result chan string = make(chan string, 1)
    for index := 0;  index< 3; index++ {
        go doRequest(result)
    }

    res, ok := <-result
    if ok {
        fmt.Println("received ", res)
    }

}

func doRequest(result chan string)  {
    response := "http response"
    defer func() {
        if x := recover(); x != nil {
            fmt.Println("Unable to send: %v", x)
        }
    }()
    result <- response
    close(result)
}
