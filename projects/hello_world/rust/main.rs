fn main() -> anyhow::Result<()> {
    let output = your_crate::run()?;
    println!("{output}");
    Ok(())
}