use ahash::{AHashMap, AHashSet};
use std::{
    mem,
    ops::{Deref, DerefMut},
};

#[derive(Clone, Copy, Debug, Eq, Hash, Ord, PartialEq, PartialOrd)]
pub struct Clause(u128, u128, u128);

#[derive(Clone, Debug, Eq, PartialEq)]
#[must_use = "iterators are lazy and do nothing unless consumed"]
pub struct ClauseLiterals(Clause);

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct ColorCNF {
    cnf: AHashSet<Clause>,
}

#[derive(Clone, Debug, Eq, PartialEq)]
pub struct CNF {
    assigned: Vec<Vec<usize>>,
    cnfs: Vec<ColorCNF>,
    possibilities: Vec<Vec<usize>>,
}

impl Clause {
    pub const MAX_SIZE: usize = 3 * u128::BITS as usize;
    pub const EMPTY: Self = Self(0, 0, 0);

    #[inline]
    pub fn add_literal(&mut self, x: usize) {
        let (bit_set, x) = self.corresponding_mut(x);
        *bit_set |= 1 << x;
    }

    #[inline]
    pub const fn complement(&self) -> Self {
        Self(!self.0, !self.1, !self.2)
    }

    #[inline]
    pub fn contains(&self, x: usize) -> bool {
        let (bit_set, x) = self.corresponding(x);
        *bit_set & (1 << x) != 0
    }

    #[inline]
    pub const fn intersection(&self, other: &Self) -> Self {
        Self(self.0 & other.0, self.1 & other.1, self.2 & other.2)
    }

    #[inline]
    pub fn intersection_update(&mut self, other: &Self) {
        self.0 &= other.0;
        self.1 &= other.1;
        self.2 &= other.2;
    }

    #[inline]
    pub const fn is_included(&self, other: &Self) -> bool {
        (self.0 & other.0 == self.0) && (self.1 & other.1 == self.1) && (self.2 & other.2 == self.2)
    }

    #[inline]
    pub const fn literals(self) -> ClauseLiterals {
        ClauseLiterals(self)
    }

    #[inline]
    pub fn remove_literal(&mut self, x: usize) {
        let (bit_set, x) = self.corresponding_mut(x);
        *bit_set &= !(1 << x);
    }

    #[inline]
    pub const fn union(&self, other: &Self) -> Self {
        Self(self.0 | other.0, self.1 | other.1, self.2 | other.2)
    }

    #[inline]
    pub fn union_update(&mut self, other: &Self) {
        self.0 |= other.0;
        self.1 |= other.1;
        self.2 |= other.2;
    }

    #[inline]
    pub const fn size(&self) -> usize {
        (self.0.count_ones() + self.1.count_ones() + self.2.count_ones()) as usize
    }

    #[inline]
    fn corresponding(&self, x: usize) -> (&u128, usize) {
        if x < u128::BITS as usize {
            (&self.0, x)
        } else if x < 2 * u128::BITS as usize {
            (&self.1, x - u128::BITS as usize)
        } else {
            (&self.2, x - 2 * u128::BITS as usize)
        }
    }

    #[inline]
    fn corresponding_mut(&mut self, x: usize) -> (&mut u128, usize) {
        if x < u128::BITS as usize {
            (&mut self.0, x)
        } else if x < 2 * u128::BITS as usize {
            (&mut self.1, x - u128::BITS as usize)
        } else {
            (&mut self.2, x - 2 * u128::BITS as usize)
        }
    }

    #[inline]
    const fn min_literal(&self) -> Option<usize> {
        let x = self.0.trailing_zeros();
        if x != u128::BITS {
            return Some(x as usize);
        }
        let x = self.1.trailing_zeros();
        if x != u128::BITS {
            return Some((x + u128::BITS) as usize);
        }
        let x = self.2.trailing_zeros();
        if x != u128::BITS {
            return Some((x + 2 * u128::BITS) as usize);
        }
        None
    }
}

impl From<&[usize]> for Clause {
    fn from(v: &[usize]) -> Self {
        let mut clause = Self::EMPTY;
        for &x in v {
            clause.add_literal(x);
        }
        clause
    }
}

impl Deref for ClauseLiterals {
    type Target = Clause;

    #[inline(always)]
    fn deref(&self) -> &Self::Target {
        &self.0
    }
}

impl DerefMut for ClauseLiterals {
    #[inline(always)]
    fn deref_mut(&mut self) -> &mut Self::Target {
        &mut self.0
    }
}

impl Iterator for ClauseLiterals {
    type Item = usize;

    #[inline]
    fn next(&mut self) -> Option<Self::Item> {
        let x = self.min_literal()?;
        self.remove_literal(x);
        Some(x)
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        let size = self.size();
        (size, Some(size))
    }
}

impl ColorCNF {
    pub fn add(&mut self, clause: Clause) {
        self.cnf.insert(clause);
    }

    pub fn assignments(&mut self, to_others: &[usize], to_self: &[usize]) {
        let to_others = Clause::from(to_others);
        let to_self = Clause::from(to_self).complement();
        self.cnf = self
            .cnf
            .iter()
            .filter_map(|clause| {
                if clause.intersection(&to_others) == Clause::EMPTY {
                    Some(clause.intersection(&to_self))
                } else {
                    None
                }
            })
            .collect()
    }

    pub fn len(&self) -> usize {
        self.cnf.len()
    }

    pub fn new() -> Self {
        Self {
            cnf: AHashSet::new(),
        }
    }

    pub fn pure_literals(&self, assigned: &[usize]) -> Vec<usize> {
        let assigned = Clause::from(assigned);
        self.cnf
            .iter()
            .fold(assigned, |acc, clause| acc.union(clause))
            .complement()
            .literals()
            .collect()
    }

    pub fn remove_non_minimal(&mut self) {
        let (clauses, mut map) = self.clauses_with_id();
        let target_size = clauses[clauses.len() - 1].size();
        let stop = clauses.partition_point(|clause| clause.size() < target_size);
        let mut is_minimal = vec![true; clauses.len()];
        for (i, clause) in clauses[..stop].iter().enumerate() {
            if !is_minimal[i] {
                continue;
            }
            let mut literals = clause.literals();
            let mut intersection = map.get(&literals.next().unwrap()).unwrap().clone();
            for x in literals {
                intersection = intersection
                    .intersection(map.get(&x).unwrap())
                    .copied()
                    .collect();
            }
            for clause_id in intersection {
                is_minimal[clause_id] = false;
                for x in clauses[clause_id].literals() {
                    map.get_mut(&x).unwrap().remove(&clause_id);
                }
            }
            is_minimal[i] = true;
        }
        self.cnf = clauses
            .into_iter()
            .zip(is_minimal.into_iter())
            .filter_map(|(clause, minimal)| if minimal { Some(clause) } else { None })
            .collect()
    }

    pub fn unit_propagation(&self) -> Vec<usize> {
        let mut single_literals = Vec::new();
        for clause in &self.cnf {
            match clause.size() {
                0 => panic!("unsatisfiable formula"),
                1 => single_literals.push(clause.min_literal().unwrap()),
                _ => (),
            }
        }
        single_literals
    }

    fn clauses_with_id(&mut self) -> (Vec<Clause>, AHashMap<usize, AHashSet<usize>>) {
        let mut temp = AHashSet::new();
        mem::swap(&mut self.cnf, &mut temp);
        let mut clauses: Vec<Clause> = temp.into_iter().collect();
        clauses.sort_by_cached_key(|clause| clause.size());
        let mut map: AHashMap<usize, AHashSet<usize>> = AHashMap::with_capacity(Clause::MAX_SIZE);
        for (i, clause) in clauses.iter().enumerate() {
            for x in clause.literals() {
                if let Some(s) = map.get_mut(&x) {
                    s.insert(i);
                } else {
                    let mut s = AHashSet::new();
                    s.insert(i);
                    map.insert(x, s);
                }
            }
        }
        map.shrink_to_fit();
        for v in map.values_mut() {
            v.shrink_to_fit();
        }
        (clauses, map)
    }
}

impl FromIterator<Clause> for ColorCNF {
    fn from_iter<I: IntoIterator<Item = Clause>>(iter: I) -> Self {
        Self {
            cnf: iter.into_iter().collect(),
        }
    }
}

impl CNF {
    pub fn assignments(&mut self) {
        for (i, (cnf, to_self)) in self.cnfs.iter_mut().zip(self.assigned.iter()).enumerate() {
            let mut to_others = Vec::with_capacity(Clause::MAX_SIZE);
            self.assigned
                .iter()
                .enumerate()
                .filter_map(|(j, assigned)| if j != i { Some(assigned) } else { None })
                .for_each(|assigned| to_others.extend_from_slice(assigned));
            cnf.assignments(&to_others, to_self)
        }
    }

    pub fn pure_literals(&mut self) -> bool {
        let mut assigned: Vec<usize> = (self.possibilities.len()..Clause::MAX_SIZE).collect();
        assigned.reserve_exact(Clause::MAX_SIZE - assigned.len());
        for color in self.assigned.iter() {
            assigned.extend_from_slice(color);
        }
        let mut literals_assigned = false;
        for (c, (cnf, color)) in self.cnfs.iter().zip(self.assigned.iter_mut()).enumerate() {
            let mut assigned = assigned.clone();
            assigned.reserve_exact(Clause::MAX_SIZE - assigned.len());
            assigned.extend(
                self.possibilities
                    .iter()
                    .enumerate()
                    .filter_map(|(i, pos)| {
                        if pos.len() > 0 && !pos.contains(&c) {
                            Some(i)
                        } else {
                            None
                        }
                    }),
            );
            let pure_literals = cnf.pure_literals(&assigned);
            literals_assigned |= pure_literals.len() > 0;
            for x in pure_literals.into_iter() {
                color.push(x);
                self.possibilities[x].clear();
                assigned.push(x);
            }
        }
        literals_assigned
    }

    pub fn remove_non_minimal(&mut self) {
        for cnf in self.cnfs.iter_mut() {
            cnf.remove_non_minimal();
        }
    }

    pub fn simplify(&mut self) {
        loop {
            self.assignments();
            if self.pure_literals() {
                continue;
            }
            if self.unit_propagation() {
                continue;
            }
            break;
        }
        self.remove_non_minimal();
    }

    pub fn unit_propagation(&mut self) -> bool {
        let mut unit_clauses = false;
        for (c, cnf) in self.cnfs.iter().enumerate() {
            let single_literals = cnf.unit_propagation();
            unit_clauses |= single_literals.len() > 0;
            for x in single_literals {
                let index = self.possibilities[x].iter().position(|&d| d == c).unwrap();
                self.possibilities[x].swap_remove(index);
            }
        }
        for (x, pos) in self.possibilities.iter_mut().enumerate() {
            if pos.len() != 1 {
                continue;
            }
            unit_clauses = true;
            let c = pos.pop().unwrap();
            self.assigned[c].push(x);
        }
        unit_clauses
    }
}
