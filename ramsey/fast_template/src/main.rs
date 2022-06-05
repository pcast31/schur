use fast_template::cliques::no_clique;
use std::time::Instant;

fn main() {
    let n = 30;
    let k = 5;

    let now = Instant::now();
    let mut clauses = no_clique(n, k);
    let elapsed = now.elapsed();
    println!("{:?} -- {:?}", elapsed, clauses.len());

    let now = Instant::now();
    clauses.remove_non_minimal();
    let elapsed = now.elapsed();
    println!("{:?} -- {:?}", elapsed, clauses.len());
}
