fn main() -> anyhow::Result<()> {
    let output = rust_lib::run()?;
    println!("{output}");
    Ok(())
}