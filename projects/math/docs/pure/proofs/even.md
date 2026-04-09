# If $n$ is even, then $n^2$ is even

**Claim:**

If $n$ is even, then $n^2$ is even.

**Proof:**

Assume $n$ is even. Then, by definition, there exists an integer $k$ such that:

$$
n=2k
$$

Then:

$$
n^2=(2k)^2
=4k^2
=2(2k)^2
$$

Since $2k^2$ is an integer, $n^2$ is divisible by $2$. Therefore, by direct example, $n^2$ is even.

**Claim:**

If $n^2$ is even, then $n$ is even.

**Proof:**

Assume $n$ is odd. Then, by definition, there exists integer $k$ such that:

$$
n=2k+1
$$

But it [has been shown](odd.md) that for odd $n$, $n^2$ is odd.

This contradicts the assumption that $n^2$ is even.

Therefore, by contradiction, $n$ must be even.
