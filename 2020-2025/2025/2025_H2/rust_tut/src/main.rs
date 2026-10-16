use std::io;

fn main() {
    println!("=== Rust Tasks ===");

    task(1, || {
        println!("Hello, Rust!");
    });

    task(2, || {
        let x: i32 = 123;
        let y: u32 = 456;
        println!("x = {}, x * 2   = {}", x, x * 2);
        println!("y = {}, y / 3.0 = {}", y, y as f64 / 3.0);
    });

    task(3, || {
        let mut input = String::new();

        println!("Enter a number:");

        io::stdin()
            .read_line(&mut input)
            .expect("Failed to read line");

        let number: i32 = input.trim().parse().expect("Please enter a valid number");
        let even_or_odd: &str = if number % 2 == 0 { "Even" } else { "Odd" };

        println!("You entered: {}. The number is {}", number, even_or_odd);
    });

    task(4, || {
        let mut v: Vec<i32> = Vec::new();
        for i in 1..=5 {
            v.push(i);
        }
        println!("{:?}", v);
    });

    task(5, || {});

    task(6, || {});

    task(7, || {});

    task(8, || {});
}

fn task<F: Fn()>(num: u32, f: F) {
    println!("\n--- Task {num} ---");
    f();
}
