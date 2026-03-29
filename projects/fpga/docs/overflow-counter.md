# Overflow Counter

An overflow counter is a counter that can overflow back to zero when it fills up.

In the overflow counter subfolder, a 32-bit overflow counter is implemented for a Basys 3 FPGA board, part number: xc7a35tcpg236-1.

The counter has 3 inputs: (1) ``clk``, (2) ``reset``, and (3) ``enable`` with the output being a 16-bit bus entity called ``led``. The counter has the following behaviour:

* At every positive (i.e., rising) edge of the ``clk`` signal, the counter's value increases by 1. This is achieved using a procedural block that will be edge-triggered by the clock. This is specified by the condition ``posedge clk``.
* For condition ``reset == 1``, the counter's value resets to 0. When ``reset == 0``, the counter increments.
* The counter increments when enabled (i.e., ``enable == 1``) and stops incrementing when disbled (``enable == 0``).

The full procedural block describing this behaviour is given by:

```
always @(posedge clk) begin
    if (reset == 1’b1) begin
        counter <= 32’d0;
    end else if (enable == 1’b1) begin
        counter <= counter + 1’b1;
    end else begin
        counter <= counter; // redundant but harmless line
    end
end
```

> **Note:**
>
> The contents of ``@(...)`` is called a sensitivity list and describes the conditions or events that will activate the process. In this case, our sensitivity list says to enter the procedural block for every rising edge of ``clk``.
>
> This type of procedural b lock is called a *clocked process* and forms the basis of practically all sequential logic designs in FPGAs. Without clocked processes, the design cannot support dynamic states (i.e., memory, operations, events or conditions that vary over time)

> **Note:**
>
> The operator ``<=`` is used to make the assignment instead of using just an equal sign. The operator ``<=`` introduces a nonblocking assignment. **You should always use nonblocking assignments inside clocked processes.**
