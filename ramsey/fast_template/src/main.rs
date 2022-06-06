use fast_template::cliques::no_clique;

fn main() {
    let n = 10;
    let k = 3;
    let clauses = no_clique(n, k);
    println!("{:?}", clauses);
}
