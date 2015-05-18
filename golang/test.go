package main

import "fmt"

func main() {
    /*pow := make([]int, 10)
    for i := range pow {
        pow[i] = 1 << uint(i)
    }
    for _, value := range pow {
        fmt.Printf("%d\n", value)
    }*/


    str := "hello, 世界"
    n := len(str)
    /*for i:=0; i<n ; i++{
        ch := str[i] //根据下标取字符，类型为byte
        fmt.Println(i, ch)
    }
    for i,ch := range str {
        fmt.Println(i, ch) //这里的ch类型为rune, 以Unicode遍历
    }*/
    fmt.Println(fmt.Sprintf("length is %d", n))

    array := [5]int{1,2,3,4,5}
    fmt.Println("array values: ", array)

    //slice := array[:3]
    var slice []int = make([]int, 2, 5)
    for i, v := range slice{
        fmt.Println("slice[", i,"]", v)
    }
    fmt.Println("len: ", len(slice))
    fmt.Println("cap: ", cap(slice))

    //slice = append(slice, 2,3)
    slice2 := []int{2,3,4,5,6}
    slice = append(slice, slice2...)
    for i, v := range slice{
        fmt.Println("slice[", i,"]", v)
    }
    fmt.Println("cap: ", cap(slice))
    for i, j := 0, len(slice)-1 ; i < j; i, j = i+1, j-1 {
        slice[i] , slice[j] = slice[j], slice[i]
    }
    fmt.Println(slice)


    type Person struct{
        id int
        name string
    }
    var persons map[string] Person
    persons = make(map[string] Person)

    persons["1"] = Person{1, "jason"}
    persons["2"] = Person{2, "LQ"}
    person, result := persons["12"]
    if result {
        fmt.Println("name is ", person.name)
    }else{
        fmt.Println("not found person")
    }
    persons["new"] = Person{3, "Nil"}
    delete(persons, "new")
    
    JLoop:
    for{
        for{
            break JLoop
        }
    }

    PrintArgs(1,2,3,4)
    PrintArgs([]int{2,3,4}...)
    PrintArgs2("int", 2, 2.0)

    /*fmt.Println("counting")
    for i := 0; i < 10; i++ {
        defer fmt.Println(i)
    }
    fmt.Println("done")*/

    var a Integer = 1
    if a.Less(2) {
        fmt.Println("Integer a < 2 !!!")
    }

}

func PrintArgs(args ...int) {
    for _, arg := range args {
        fmt.Println(arg)
    }
}

func PrintArgs2(args ...interface{}) {
    for _, arg:= range args{
        switch arg.(type) {
            case int:
                fmt.Println(arg, "is an int")
            case string:
                fmt.Println(arg, "is string")
            default:
                fmt.Println("is unknown type")
        }
    }
}

type Integer int
func (a Integer)Less(b Integer) bool {
    return a < b
}