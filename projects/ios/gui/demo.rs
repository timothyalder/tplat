use std::sync::atomic::{AtomicI32, Ordering};

static COUNTER: AtomicI32 = AtomicI32::new(0);

#[unsafe(no_mangle)]
pub extern "C" fn get_and_increment_counter() -> i32 {
    COUNTER.fetch_add(1, Ordering::SeqCst) + 1
}

#[unsafe(no_mangle)]
pub extern "C" fn print_something_from_rust() {
    println!("Ferris says hello from the UI!");
}