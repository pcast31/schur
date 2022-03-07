# Parallel Algorithms for Weak-Schur Numbers 

This repo aims to provide code using simulated annealing (and potentially other genetic algorithms) to compute weakly sum-free partitions, over multiple processes and in parallel. The upshot is that there are also reasonably fast functions which verify partitions and compute the fitness score of a given potential partition, which are completely implemented in `numpy` for speed.

## `verify_partition` and `fitness `

Both algorithms are based on the same method of generating all unique pairs of numbers in a given color partition; the idea is to generate a `meshgrid` of all possible pairs, and then get the (strictly) upper triangular part of the returned matrices of `meshgrid`: say `xx` and `yy`. The performance of this implementation of `verify_partition` is as follows.

![Performance](results/verify_partititon_times.png)

In each case, the X-axis represents the total number of iterations used by `timeit`, and the time is in seconds. As expected, the total time taken is linear in the number of iterations, but time taken per iteration remains fairly constant (and quite low, to be fair :)). 

`fitness` simply counts the number of pairs `a,b,c` such that they violate the sum-free property of the partition i.e. `a+b=c` for distinct `a,b,c`. Since the code isn't too different, the performance is not expected to be very different either. The specific times (in seconds) are in the following table.

| 10                     | 100                    | 500                   | 1000                  | 2500                | 5000                 |
| ---------------------- | ---------------------- | --------------------- | --------------------- | ------------------- | -------------------- |
| 0.00002689999999994086 | 0.00018969999999995935 | 0.0010127999999998138 | 0.0019521000000000122 | 0.00863309999999995 | 0.007054699999999858 |

## `algorithm`

The idea of this algorithm is to be simple, and parallellizable. The steps are as follows:

- **Step 1** Select the numbers to allocate in this round - usually, this is a list of `n` consecutive integers, and send them to the Process.
- **Step 2** The process will add one integer to each of the `n` partitions, and compute the fitness of each.
- **Step 3** Once the results have been computed, the solutions are chosen in some manner, in this case, with `SimulatedAnnealing`. 

<!-- ### Parallel Version 

- **Step 1** Select the numbers to allocate in this round - this is a list of `n` consecutive integers, and send them to the Process.
- **Step 2** The process will add one integer to each of the `n` partitions, and compute the fitness of each, for `k` solutions at a time.
- **Step 3** Once the results have been computed, the solutions are chosen in some manner, again, in this case, with `SimulatedAnnealing`.  -->

