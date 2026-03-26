#!/usr/bin/env node
import { spawn } from "node:child_process";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);

// Find the actual CLI script from the package
const cli = require.resolve("markdownlint-cli/markdownlint.js");

const child = spawn(process.execPath, [cli, ...process.argv.slice(2)], {
  stdio: "inherit",
});

child.on("exit", (code) => process.exit(code));