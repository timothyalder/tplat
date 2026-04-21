const { main } = require("./main");

const result = main();

if (result !== "Hello world") {
  console.error("Unexpected output:", result);
  process.exit(1);
}

console.log("Test passed");