def main() -> str:
    return "Hello world"

def test():
    assert main() == "Hello world"

if __name__ == "__main__":
    print(main())