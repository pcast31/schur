use std::{
    fmt::Debug,
    ops::{Index, IndexMut},
    sync::mpsc,
    thread,
    time::Instant,
};

const SCHUR_NUMBER: u8 = 44;
const STACK_SIZE: usize = SCHUR_NUMBER as usize - 2;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum Color {
    One,
    Two,
    Three,
    Four,
}

use Color::*;

impl Color {
    #[inline(always)]
    fn next(self) -> Option<Color> {
        match self {
            One => Some(Two),
            Two => Some(Three),
            Three => Some(Four),
            Four => None,
        }
    }
}

trait SumFreeSubset
where
    Self: Copy + Debug + Eq,
{
    fn can_add(self, n: u8) -> bool;

    unsafe fn add(self, n: u8) -> Self;

    fn try_add(self, n: u8) -> Option<Self>;
}

impl SumFreeSubset for u64 {
    #[inline(always)]
    fn can_add(self, n: u8) -> bool {
        self & (self.reverse_bits() >> (0x3f & !n)) == 0
    }

    #[inline(always)]
    unsafe fn add(self, n: u8) -> Self {
        self | (1 << n)
    }

    #[inline(always)]
    fn try_add(self, n: u8) -> Option<Self> {
        if self.can_add(n) {
            Some(unsafe { self.add(n) })
        } else {
            None
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
struct Partition<T>(u8, T, T, T, T)
where
    T: SumFreeSubset;

impl<T> Index<Color> for Partition<T>
where
    T: SumFreeSubset,
{
    type Output = T;

    #[inline(always)]
    fn index(&self, color: Color) -> &Self::Output {
        match color {
            One => &self.1,
            Two => &self.2,
            Three => &self.3,
            Four => &self.4,
        }
    }
}

impl<T> IndexMut<Color> for Partition<T>
where
    T: SumFreeSubset,
{
    #[inline(always)]
    fn index_mut(&mut self, color: Color) -> &mut Self::Output {
        match color {
            One => &mut self.1,
            Two => &mut self.2,
            Three => &mut self.3,
            Four => &mut self.4,
        }
    }
}

impl<T> Partition<T>
where
    T: SumFreeSubset,
{
    #[inline(always)]
    fn try_add(mut self, color: Color) -> Option<Self> {
        let subset = self[color].try_add(self.0)?;
        self[color] = subset;
        self.0 += 1;
        Some(self)
    }
}

type Node<T> = (Color, Partition<T>);

#[derive(Clone, Debug, Eq, PartialEq)]
struct Stack<T>(usize, [Node<T>; STACK_SIZE])
where
    T: SumFreeSubset;

impl<T> Stack<T>
where
    T: SumFreeSubset,
{
    fn new(partition: Partition<T>) -> Self {
        Stack(1, [(One, partition); STACK_SIZE])
    }

    #[inline(always)]
    fn pop(&mut self) -> Option<Node<T>> {
        if self.0 == 0 {
            None
        } else {
            self.0 -= 1;
            Some(unsafe { *self.1.get_unchecked(self.0) })
        }
    }

    #[inline(always)]
    fn push(&mut self, node: Node<T>) {
        unsafe {
            *self.1.get_unchecked_mut(self.0) = node;
        }
        self.0 += 1;
    }
}

fn dfs<T>(partition: Partition<T>) -> Vec<Partition<T>> where T: SumFreeSubset {
    let mut solutions = Vec::new();
    let mut stack = Stack::new(partition);

    while let Some((color, partition)) = stack.pop() {
        if let Some(next_color) = color.next() {
            stack.push((next_color, partition));
        }
        if let Some(extended) = partition.try_add(color) {
            if partition.0 == SCHUR_NUMBER {
                solutions.push(partition);
            } else {
                stack.push((One, extended));
            }
        }
    }
    solutions
}

fn main() {
    const PARTITIONS: [Partition<u64>; 6] = [
        Partition(5, 0b1010, 0b100, 0b10000, 0),
        Partition(6, 0b10010, 0b1100, 0b100000, 0),
        Partition(5, 0b10, 0b1100, 0b10000, 0),
        Partition(5, 0b10010, 0b100, 0b1000, 0),
        Partition(5, 0b10, 0b100, 0b11000, 0),
        Partition(5, 0b10, 0b100, 0b1000, 0b10000),
    ];

    println!("Looking for solutions.");

    let start = Instant::now();
    let (tx, rx) = mpsc::channel();

    for &partition in PARTITIONS.iter() {
        let tx = tx.clone();
        thread::spawn(move || {
            let partitions = dfs(partition);
            tx.send(partitions).unwrap();
        });
    }

    let mut solutions = Vec::new();

    for _ in 0..PARTITIONS.len() {
        let new_solutions = rx.recv().unwrap();
        solutions.extend(new_solutions);
    }

    let duration = start.elapsed();

    println!("{} partitions found in {:?}.", solutions.len(), duration);
    println!("Writting solutions.");

    // TODO : write solutions

    println!("Done.");
}
