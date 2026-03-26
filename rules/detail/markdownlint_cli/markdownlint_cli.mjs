#!/usr/bin/env node
import { main } from "markdownlint-cli";

async function run() {
  const args = process.argv.slice(2);
  const exitCode = await main(args);
  process.exit(exitCode);
}

run();
