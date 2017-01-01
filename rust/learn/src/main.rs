fn main() {
    // 赋值， mut表示可mutable, i32表示类型，有类型推断
    let mut x: i32 = 10;
    x += 23;
    // 更多参数打印格式： https://doc.rust-lang.org/stable/std/fmt/
    println!("Hello, world! {}", x);

    // res 没有被使用，加上前缀 _ 可以抑制编译器警告
    let _res = print_sum(1, 2);
    println!("returned sum is {}", _res);

    // panic
    // diverges()
    // 发散函数可以被用作任何类型：
    // let panic: i32 = diverges();

    test_fn_pointer();

    test_array();

    test_borrow();
    test_ref();
}



// 函数声明，参数必须指定类型; 函数只能有一个返回值
fn print_sum(x: i32, y: i32) -> i32 {
    println!("sum is: {}", x + y);

    // 不能最后加上分号; 因为分号是表达式的分隔符，如果加了分号，表示后面还有一个空的表达式，即返回一个 () 空
    // 加不加return都可以
    x + y
}

// 发散函数，不返回
// fn diverges() -> ! {
//     panic!("This function never returns!");
// }

fn test_fn_pointer(){
    // 声明一个函数类型的变量
    let function: fn(i32)->i32;
    function = plus_one;
    let res = function(1);
    println!("fn(1) {}", res);
}

fn plus_one(i: i32) -> i32 {
    i + 1
}

fn test_array(){
    let mut a: [i32; 4] = [1, 2, 3, 4]; // [i32; 4]
    println!("a[0] is {}", a[0]);
    a = [10; 4]; // 10, 10, 10
    println!("a has {} elements", a.len());

    let names: [&str; 3] = ["Graydon", "Brian", "Niko"]; // names: [&str; 3]
    println!("The second name is: {}", names[1]);

    // slice
    let b = [1,2,3,4,5];
    let complete = &b[..]; // A slice containing all of the elements in a
    println!("b[..] is {}", complete[0]);
    let middle = &b[1..2]; // A slice of a: just the elements 
    println!("b[1..2] is {}, len is {}", middle[0], middle.len());

    // tuple
    let x = (1, 2); // x: (i32, i32)
    let (_x1, _x2) = x;
    let _x0 = x.0;
}

fn test_borrow(){
    // x 和 y 必须在同一scope中，因为 y 是 x 的 reference, x 被回收的话，y就没有意义了，编译器会报错。
    // x 必须声明在 y 的前面
    let x = 5;
    let y: &i32;
    y = &x;

    println!("{}", y);
}

fn test_ref(){
    let mut x = 5;
    {
        let y = &mut x;
        *y += 1;
    }
    println!("{}", x);
}