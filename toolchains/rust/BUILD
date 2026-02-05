load("@rules_rust//crate_universe:defs.bzl", "crates_vendor")

alias(
    name = "cargo_toml",
    actual = "Cargo.toml",
)

crates_vendor(
    name = "vendor",
    cargo_lockfile = "Cargo.lock",
    generate_build_scripts = True,
    manifests = ["Cargo.toml"],
    mode = "remote",
    tags = ["manual"],
)