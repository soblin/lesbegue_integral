# Approximation of Lesbegue Integral

This program visualizes the curve $f: x \rightarrow y$ in terms of discretized `(xs, ys)`, divides `ys` in the following way

$$
A_{n, k} = \\{x \mid k \cdot 2 ^ {-n} \leq y \leq(k+1) \cdot 2 ^ {-n} \\},
$$

and then approximates f by the following series

$$
\sum_{k = 0} ^ {n \cdot 2 ^ n} k \cdot 2 ^ {-n} \chi(A_{n, k}),
$$

where $\chi$ is the characteristic function.
