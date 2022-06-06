use crate::sat::{Clause, ColorCNF};

#[derive(Clone, Debug)]
#[must_use = "iterators are lazy and do nothing unless consumed"]
struct PartialPermutations {
    cycles: Vec<usize>,
    perm: Vec<usize>,
    n: usize,
    size: usize,
}

impl PartialPermutations {
    fn new(n: usize, size: usize) -> Self {
        assert!(size > 1);
        assert!(n >= size);
        let mut cycles: Vec<usize> = (n - size + 1..=n).rev().collect();
        cycles[size - 1] += 1;
        let mut perm: Vec<usize> = (1..=n).collect();
        perm.swap(size - 1, n + 1 - cycles[size - 1]);
        Self {
            cycles,
            perm,
            n,
            size,
        }
    }
}

impl Iterator for PartialPermutations {
    type Item = Vec<usize>;

    fn next(&mut self) -> Option<Self::Item> {
        for (i, x) in self.cycles.iter_mut().enumerate().rev() {
            if *x == 1 {
                self.perm[i..].rotate_left(1);
                *x = self.n - i;
            } else {
                *x -= 1;
                self.perm.swap(i, self.n - *x);
                return Some(self.perm[..self.size].to_vec());
            }
        }
        None
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        let n_perms = (self.n - self.size + 1..=self.size).fold(Some(1), |x: Option<usize>, y| {
            if let Some(x) = x {
                x.checked_mul(y)
            } else {
                None
            }
        });
        (0, n_perms)
    }
}

fn all_diffs(perm: &[usize], n: usize) -> Clause {
    let mut clause = Clause::from(perm);
    for (i, &x) in perm.iter().enumerate() {
        for &y in perm[i + 1..].iter() {
            let literal = if x < y { y - x } else { n + y - x };
            clause.add_literal(literal);
        }
    }
    clause
}

pub fn no_clique(n: usize, k: usize) -> ColorCNF {
    PartialPermutations::new(n, k - 1)
        .map(|perm| all_diffs(&perm, n))
        .collect()
}
