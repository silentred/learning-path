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

    test_fn_pointer()
}



// 函数声明，参数必须指定类型; 函数只能有一个返回值
fn print_sum(x: i32, y: i32) -> i32 {
    println!("sum is: {}", x + y);

    // 不能最后加上分号; 因为分号是表达式的分隔符，如果加了分号，表示后面还有一个空的表达式，即返回一个{} 空
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
