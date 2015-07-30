package main

import (
    "gopkg.in/gorp.v1"
    _ "github.com/go-sql-driver/mysql"
    "database/sql"
    "log"
    "fmt"
)

func main()  {
    dbmap := initDb()

    //选择多行
    var posts []Post
    // var posts []struct{
    //     Id      int64  `db:"id"`
    //     Title   string `db:"title"`
    //     Content    string `db:"content"`
    // 结构可以包含结果中没有的字段
    // }
    _, err := dbmap.Select(&posts, "select * from post_test order by id")
    checkErr(err, "select failed")
    // 这里的_为index,忽略
    for _ , post := range posts {
        fmt.Printf("Post Id:%d, Title: %s, Created At: %s \n", post.Id, post.Title, post.CreatedAt)
    }

    // var post2 struct{
    //     Id      int64
    //     Title   string
    //     Content    string
    // }
    // err = dbmap.SelectOne(&post2, "select * from post_test where id=?", 2)
    // checkErr(err, "no result")
    // fmt.Printf("Post Id:%d, Title: %s \n", post2.Id, post2.Title)

    //根据id取单行； 这里_为err，忽略
    // obj, _ := dbmap.Get(Post{}, 1)
    // post := obj.(*Post)
    // fmt.Println("Post Id=1, Title is " + post.Title)


}

func initDb() *gorp.DbMap {
    db, err := sql.Open("mysql", "root:@tcp(localhost:3306)/test?charset=utf8")
    checkErr(err, "open db failed")
    // construct a gorp DbMap
    dbmap := &gorp.DbMap{Db: db, Dialect: gorp.MySQLDialect{"InnoDB", "UTF8"}}
    //dbmap.AddTableWithName(Post{}, "post_test").SetKeys(true, "Id")
    return dbmap
}


type Post struct {
    // db tag lets you specify the column name if it differs from the struct field
    Id      int64  `db:"id"`
    Title   string `db:"title"`               // Column size set to 50
    Content    string `db:"content"` // Set both column name and size
    CreatedAt   string `db:"created_at"`
    IgnoreMe   string    `db:"-"`
}

func newPost(title, body string) Post {
    return Post{
        Title:   title,
        Content:    body,
    }
}
// This is equivalent to using the ColMap methods:
//
//   table := dbmap.AddTableWithName(Product{}, "product")
//   table.ColMap("Id").Rename("product_id")
//   table.ColMap("Price").Rename("unit_price")
//   table.ColMap("IgnoreMe").SetTransient(true)
type Product struct {
    Id         int64     `db:"product_id, primarykey, autoincrement"`
    Price      int64     `db:"unit_price"`
    IgnoreMe   string    `db:"-"`
}

func checkErr(err error, msg string) {
    if err != nil {
        log.Fatalln(msg, err)
    }
}
