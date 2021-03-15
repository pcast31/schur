use std::{
    fmt::Debug,
    fs::File,
    io::{self, Write},
    ops::{Index, IndexMut},
    sync::mpsc,
    thread,
    time::Instant,
};

const SCHUR_NUMBER: u8 = 66;
const STACK_SIZE: usize = SCHUR_NUMBER as usize + 1;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
enum Color {
    One,
    Two,
    Three,
    Four,
}

use Color::*;

impl Color {
    fn all() -> <Vec<Self> as IntoIterator>::IntoIter {
        let mut all_colors = vec![One];

        while let Some(color) = all_colors.last().unwrap().next() {
            all_colors.push(color);
        }
        all_colors.into_iter()
    }

    #[inline(always)]
    fn next(self) -> Option<Self> {
        match self {
            One => Some(Two),
            Two => Some(Three),
            Three => Some(Four),
            Four => None,
        }
    }
}

trait WeaklySumFreeSubset
where
    Self: Copy + Debug + Eq + Ord,
{
    fn can_add(self, n: u8) -> bool;

    unsafe fn add(self, n: u8) -> Self;

    fn try_add(self, n: u8) -> Option<Self>;

    fn to_vec(self) -> Vec<usize>;

    fn to_string(self) -> String {
        self.to_vec()
            .iter()
            .map(|n| n.to_string())
            .collect::<Vec<String>>()
            .join(" ")
    }
}

impl WeaklySumFreeSubset for u128 {
    #[inline(always)]
    fn can_add(self, n: u8) -> bool {
        if n & 1 == 1 {
            self & (self.reverse_bits() >> (0x7f & !n)) == 0
        } else {
            (self & (self.reverse_bits() >> (0x7f & !n))) & !(1 << (n >> 1)) == 0
        }
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

    fn to_vec(mut self) -> Vec<usize> {
        let mut partition = Vec::new();
        let mut n = 0;

        while self > 0 {
            if self & 1 == 1 {
                partition.push(n);
            }
            self >>= 1;
            n += 1;
        }
        partition
    }
}

#[derive(Clone, Copy, Debug, Eq, Ord, PartialEq, PartialOrd)]
struct Partition<S>(u8, S, S, S, S)
where
    S: WeaklySumFreeSubset;

impl<S> Index<Color> for Partition<S>
where
    S: WeaklySumFreeSubset,
{
    type Output = S;

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

impl<S> IndexMut<Color> for Partition<S>
where
    S: WeaklySumFreeSubset,
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

impl<S> IntoIterator for Partition<S>
where
    S: WeaklySumFreeSubset,
{
    type Item = S;
    type IntoIter = <Vec<Self::Item> as IntoIterator>::IntoIter;

    fn into_iter(self) -> Self::IntoIter {
        Color::all()
            .map(|color| self[color])
            .collect::<Vec<Self::Item>>()
            .into_iter()
    }
}

impl<S> Partition<S>
where
    S: WeaklySumFreeSubset,
{
    #[inline(always)]
    fn try_add(mut self, color: Color) -> Option<Self> {
        let subset = self[color].try_add(self.0)?;
        self[color] = subset;
        self.0 += 1;
        Some(self)
    }

    fn to_string(self) -> String {
        self.into_iter()
            .map(|subset| subset.to_string())
            .collect::<Vec<String>>()
            .join("\n")
    }
}

type Node<S> = (Color, Partition<S>);

#[derive(Clone, Debug, Eq, PartialEq)]
struct Stack<S>(usize, [Node<S>; STACK_SIZE])
where
    S: WeaklySumFreeSubset;

impl<S> Stack<S>
where
    S: WeaklySumFreeSubset,
{
    fn new(partition: Partition<S>) -> Self {
        Stack(1, [(One, partition); STACK_SIZE])
    }

    #[inline(always)]
    fn pop(&mut self) -> Option<Node<S>> {
        if self.0 == 0 {
            None
        } else {
            self.0 -= 1;
            Some(unsafe { *self.1.get_unchecked(self.0) })
        }
    }

    #[inline(always)]
    fn push(&mut self, node: Node<S>) {
        unsafe {
            *self.1.get_unchecked_mut(self.0) = node;
        }
        self.0 += 1;
    }
}

fn dfs<S>(partition: Partition<S>) -> Vec<Partition<S>>
where
    S: WeaklySumFreeSubset,
{
    let mut solutions = Vec::new();
    let mut stack = Stack::new(partition);

    while let Some((color, partition)) = stack.pop() {
        if partition.0 == SCHUR_NUMBER + 1 {
            solutions.push(partition);
            continue;
        }
        if let Some(next_color) = color.next() {
            stack.push((next_color, partition));
        }
        if let Some(extended) = partition.try_add(color) {
            stack.push((One, extended));
        }
    }
    solutions
}

fn find_solutions() -> Vec<Partition<u128>> {
    const PARTITIONS: [Partition<u128>; 5] = [
        Partition(33, 0x2400916, 0xa800e8, 0x17f600, 0x1fd000000),
        Partition(33, 0x102400916, 0xa800e8, 0x17f600, 0xfd000000),
        Partition(32, 0x2410916, 0xa800e8, 0x16f600, 0xfd000000),
        Partition(32, 0x82410916, 0xa800e8, 0x16f600, 0x7d000000),
        Partition(32, 0x82400916, 0xa800e8, 0x17f600, 0x7d000000),
    ];

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

    solutions
}

fn write_solutions<S>(mut partitions: Vec<Partition<S>>) -> io::Result<()>
where
    S: WeaklySumFreeSubset,
{
    partitions.sort_unstable();
    let name_width = partitions.len().to_string().len();

    for (num, partition) in partitions.iter().enumerate() {
        let mut file = File::create(format!(
            "partitions/{:0width$}.txt",
            num + 1,
            width = name_width
        ))?;
        let content = partition.to_string().into_bytes();
        file.write(&content)?;
    }
    Ok(())
}

fn main() {
    println!("Looking for solutions.");

    let start = Instant::now();

    let solutions = find_solutions();

    let duration = start.elapsed();

    println!("{} partitions found in {:?}.", solutions.len(), duration);
    println!("Writting solutions.");

    match write_solutions(solutions) {
        Ok(()) => println!("Done."),
        Err(err) => println!("Failed to write solutions.\n{}", err),
    }
}
