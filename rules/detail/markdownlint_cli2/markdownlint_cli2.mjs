#!/usr/bin/env node
import { main } from "markdownlint-cli2";

async function run() {
  const args = process.argv.slice(2);
  const exitCode = await main(args);
  process.exit(exitCode);
}

run();
