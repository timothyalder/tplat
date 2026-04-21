require_relative "hello"

result = hello

if result != "Hello world"
  STDERR.puts "Unexpected result: #{result}"
  exit 1
end

puts "Test passed"