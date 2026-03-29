# 1-bit Full Addder

A full adder is an adder with carry-in and carry-out ports. The truth table for a 1-bit full adder is shown in **Table 1**.

**Table 1:** Truth table for a 1-bit full adder.

| X | Y | C_in | Z | C_out |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 0 | 1 | 0 |
| 1 | 0 | 0 | 1 | 0 |
| 1 | 1 | 0 | 0 | 1 |
| 0 | 0 | 1 | 1 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 | 1 |

As shown in Table 1, the output $Z$ is the binary addition of $X + Y + C_{in}$, and the output $C_{out}$ is the carry bit of the addition.

The Karnaugh map for the truth table of output Z is shown in Table 2.

| C_in\XY | 00 | 10 | 11 | 01 |
| --- | --- | --- | --- | --- |
| **0** | 0 | 1 | 0 | 1 |
| **1** | 1 | 0 | 1 | 0 |

The simplified Boolean expression is $Z = (X\cdot Y'\cdot C'_{in}) + (X'\cdot Y\cdot C'_{in}) + (X'\cdot Y'\cdot C_{in}) + (X\cdot Y\cdot C_{in})$

The Karnaugh map for the truth table of output $C_{out}$ is shown in Table 3.

| C_in\XY | 00 | 10 | 11 | 01 |
| --- | --- | --- | --- | --- |
| **0** | 0 | 0 | 1 | 0 |
| **1** | 0 | 1 | 1 | 1 |

The simplified Boolean expression is $C_{out} = (X\cdot Y) + (X\cdot C_{in}) + (Y\cdot C_{in})$

In the full-adder subfolder, this schematic is implemented in Vivado for a Basys 3 FPGA board, part number: xc7a35tcpg236-1.
