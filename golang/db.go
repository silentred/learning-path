package main

import (
    _ "github.com/go-sql-driver/mysql"
    "database/sql"
    "fmt"
)

func main() {
    db, err := sql.Open("mysql", "root:@tcp(localhost:3306)/test?charset=utf8")
    checkErr(err)
    //一般是不需要关闭DB的。Open不会创建连接，而是验证参数合法性。返回的db对于多协程是安全的，
    // 并且维护自己的连接池。所以Open只能调用一次，而且一般不需要Close，因为这个连接池需要被多个协程共用
    defer db.Close()

    // Open doesn't open a connection. Validate DSN data:
    err = db.Ping()
    checkErr(err)

// 插入数据
    // // Prepare statement for inserting data
    // stmtIns, err := db.Prepare("INSERT INTO note (name) VALUES( ? )") // ? = placeholder
    // checkErr(err)
    // defer stmtIns.Close() // Close the statement when we leave main() / the program terminates
    //
    // // Prepare statement for reading data
    // stmtOut, err := db.Prepare("SELECT * FROM note WHERE id = ?")
    // checkErr(err)
    // defer stmtOut.Close()
    //
    // // Insert square numbers for 0-24 in the database
    // for i := 10; i < 25; i++ {
    //     _, err = stmtIns.Exec((i*i)) // Insert tuples (i^2)
    //     checkErr(err)
    // }

//取数据;
    //Execute the query
    rows, err := db.Query("SELECT * FROM note limit 0, 5")
    checkErr(err)

    columns, err := rows.Columns()
    checkErr(err)

    values := make([]sql.RawBytes, len(columns))

    scanArgs := make([]interface{}, len(values))
    for i := range values {
        scanArgs[i] = &values[i]
    }

    for rows.Next() {
        // get RawBytes from data
        err = rows.Scan(scanArgs...)
        if err != nil {
            panic(err.Error()) // proper error handling instead of panic in your app
        }

        // Now do something with the data.
        // Here we just print each column as a string.
        var value string
        for i, col := range values {
            value = string(col)
            fmt.Println(columns[i], ": ", value)
        }
        fmt.Println("-----------------------------------")
    }
    if err = rows.Err(); err != nil {
        panic(err.Error()) // proper error handling instead of panic in your app
    }


}

//查看err
func checkErr(err error) {
    if err != nil {
        panic(err)
    }
}
