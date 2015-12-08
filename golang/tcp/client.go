package main

import(
    "net"
    "log"
    "time"
)

func establishConn(i int) net.Conn {
    conn, err := net.Dial("tcp", ":8888")
    if err != nil {
        log.Printf("%d: dial error: %s", i, err)
        return nil
    }
    log.Println(i, ":connect to server ok")
    return conn
}

func main() {
    var sl []net.Conn
    for i := 1; i < 500; i++ {
        conn := establishConn(i)
        if conn != nil {
            sl = append(sl, conn)
        }
    }

    time.Sleep(time.Second * 10000)
}
