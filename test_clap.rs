use clap::Parser;

#[derive(Parser)]
struct Args {
    #[arg(short = "ls")]
    list: bool,
}

fn main() {}
