pub fn run() -> anyhow::Result<String> {
    Ok("Hello world".to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_run() {
        let result = run().unwrap();
        assert_eq!(result, "Hello world");
    }
}