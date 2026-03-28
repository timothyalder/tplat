#!/usr/bin/env node

import { createRequire } from "node:module";

console.error("CWD:", process.cwd());
console.error("ARGS:", process.argv.slice(2));
const require = createRequire(import.meta.url);

// Resolve the actual CLI
const cli = require.resolve("markdownlint-cli/markdownlint");

// Forward execution
await import(cli);