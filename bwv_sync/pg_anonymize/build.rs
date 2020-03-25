use std::env;
use std::path::Path;
use std::io::Write;

fn main() {
    let out_dir = env::var("OUT_DIR").unwrap();

    // Generate array of given names
    {
        let dest = Path::new(&out_dir).join("given_names.rs");
        let mut f = std::fs::File::create(&dest).unwrap();

        const NAMES: &str = include_str!("data/given_names.txt");
        f.write_all(b"&[").unwrap();
        for name in NAMES.split("\n") {
            f.write_all(format!("\"{}\", ", name).as_bytes()).unwrap();
        }
        f.write_all(b"]").unwrap();
    }

    // Generate array of surnames
    {
        let dest = Path::new(&out_dir).join("surnames.rs");
        let mut f = std::fs::File::create(&dest).unwrap();

        const NAMES: &str = include_str!("data/surnames.txt");
        f.write_all(b"&[").unwrap();
        for name in NAMES.split("\n") {
            f.write_all(format!("\"{}\", ", name).as_bytes()).unwrap();
        }
        f.write_all(b"]").unwrap();
    }
}
