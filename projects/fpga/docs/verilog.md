# Verilog

## Keywords

### wire

``wire`` keyword represents a physical wire in a circuit and is used to connect gates or modules.

``wire`` is a type of net that describes digital signals connecting multiple hardware elements.

``wire`` does not store its value but must be driven by a continuous assignment statement ``assign`` or by connecting it to the output of a gate or module.

Value of a wire can be read or assigned inside a module but **never inside procedural code** such as ``intial`` or ``always`` blocks.

``wire`` must be a bit or a bus.

```
wire c // simple wire
assign c = a || b; // a or b
wire [9:0] A; // a cable (vector) of 10 wires
```

### assign

``assign`` describes an interconnection between wires.

Allows you to connect inputs and output directly, without the need for a procedural block.

Values are immediately updated whenever the input values change. Continuous assignment, meaning:

* order does not matter
* must avoid feedback

**You cannot use ``assign`` to allocate value to a ``reg``**

```
wire K, X, Y, Z;
wire [3:0] W;
assign W=4'd15;
assign X=Y+Z;
assign K=Y&Z;
```

Multiple driver issue:

```
wire X, Y;
assign Y=X;
assign Y=~X;
```

Feedback issue:

```
wire Z;
assign Z=~Z;
```

### reg

``reg`` is a data object that holds its value from one procedural assignment to the next.

It does not necessarily imply a physical register or flip-flop.

It can be used to store values of both sequential and combinational logic.

Its value can always only be assigned inside the module where it is declared or by a procedural block like ``always`` and ``initial``.

```
reg a; // single 1-bit register variable
reg [7:0] tom; // an 8-bit vector; a bank of 8 registers
reg [5:0] b, c; // two 6-bit variables
```

### wire vs reg

```
module my_module (
input a, input b, input reset, input enable, input clk, output reg c, output wire [3:0] led);
    reg d;
    reg [3:0] count

    // combinational logic
    always @(*) begin
        if (a & b) d = 1;
        else d = 0;
        if (a | b) c = d;
    end

    // sequential logic
    always @(posedge clk) begin
        if (reset) count <= 4'b0000;
        else if (enable) count <= count + 1;
    end
        assign led = count;
endmodule
```

### input, output, inout

Define input, output, and bidirectional ports of a module through which it communicates with the outside world or other modules.

An input port can only be read and its value cannot be changed by the module.

Input and inout ports are of type ``wire``.

Output can be ``wire`` or ``reg`` depending on how the signal is generated inside the module.

Defaults to ``wire``.

```
module Mymod (X,Y,Z);
    input wire X, Y;
    output wire Z;
    wire W;
    assign Z = Y & W;
    assign W = ~(X); // order? X is input so assume W gets set before Z?
endmodule
```

### parameter

Defines a constant that can be used throughout the design or can be set when you instantiate a module.

Allows customisation of a module during instantiation.

Can be used to define constants that are used multiple times in the design, such as clock periods, bus widths, or memory depths.

Parameters can be specified as integers, real numbers, or strings.

```
parameter n = 4;
...
reg [n-1:0] harry; // A 4-bit register whose length is set by paramater n above
```

## Number Specification

Two types of number specification in Verilog: sized and unsized.

``<size>'<base format><number>``

``<size>`` is written only in decimal and specifies the number of bits in the number.

``<base format>`` can be decimal (d or D), hexadecimal (h or H), binary (b or B) and octal (o or O). By default, is decimal.

``<number>`` is string of digits of base given in ``<base format>``

```
8'b00000101;
8'b101; // leading zeros omitted
8'h2C;
8'0001001110; redundant two leading zeros
4'bz;
12'habc;
16'd255;
```

## Operators

Operators are ``unary``, ``binary`` or ``ternary``.

### Arithmetic Operators

```
+ (addition)
- (subtraction)
* (multiplication)
/ (division)
% (modulo)
```

### Relational Operators

```
< (less than)
<= (less than or equal to)
> (greater than)
>= (greater than or equal to)
== (equal to)
!= (not equal to)
```

### Bit-wise Operators

```
~ (bitwise NOT)
& (bitwise AND)
| (bitwise OR)
^ (bitwise XOR)
~^ or ^~ (bitwise XNOR)
```

### Logical Operators

```
! (logical NOT)
&& (logical AND)
|| (logical OR)
```

### Reduction Operators

Perform a reduction operation on a vector operand and returns a single result.

```
& (reduction AND)
| (reduction OR)
~& (reduction NAND)
~| (reduction NOR)
^ (reduction XOR)
~^ or ^~ (reduction XNOR)
```

### Shift Operators

```
<< (shift left)
>> (shift right)
```

### Conditional Operators

Conditional operators ``?`` evaluates one of the two expressions based on a condition. It synthesises to a MUX.

``(cond)?(result if cond true):(result if cond false)``

```
assign a = (g) ? x : y; // a==x if g else y
```

## Procedural Block

### always

Verilog supports behavioural design, i.e., a description of what a module does. This is done through blocks of procedural code, which are introduced by the keyword ``always``.

``always`` can be used to imply both sequential and combinational logic.

Procedural statements execute sequentially, but ``always`` block itself execute concurrently with other statements in the same module.

```
always @ (sensitivity list)
    begin
        ... procedural statements ...
    end
```

Sensitivity list is a list of signals. The ``always`` block is executed whenever one of these signals changes. ``*`` is a special one-fits-all.

**Left hand terms in assignments inside an ``always`` block are always of type ``reg``.**

Different procedural statements can be include in the ``always`` block:

* ``if ... else``
* ``case``
* ``for`` loop
* ``while`` loop

#### Combinational Logic

Combinational logic is defined using an ``always @ (*)`` block. In this case, the sensitivity list automatically includes all signals found on the RHS of any assignment or as the argument of functions.

Statements in such block are executed in zero "circuit time", so you have to be careful not to create feedback loops. For example:

```
always @ (*) begin
    X = Y | Z;
    Y = X ^ W;
end
```

In the above case, each time the block is executed the value of a RHS term is changed (actually, two: X, Y), causing the block to be executed again for infinity.

#### Sequential Logic

Defined using:

```
always @ (posedge <event>)
always @ (negedge <event>)
```

## Blocking and Non-Blocking Assignments

Blocking assignments ``=`` mean the right side expression is evaluated and assigned to the left-hand side variable immediately, blocking any other assignments until complete. The next statement in the procedural block cannot be executed until the blocking assignment is completed.

* Typically used to model combinational logic.

Non-blocking assignments ``<=`` mean the right side expression is evaluated but the value is not assigned until all other assignments in the same procedural block have been evaluated. Other statements can be executed in parallel with the non-blocking assignment.

* Typically used to model sequential logic and concurrent data transfers
* Used in procedural block of type ``always @ (posedge clk)``

**It is recommended that blocking and non-blocking assignments not be mixed in the same procedural ``always`` block.**
