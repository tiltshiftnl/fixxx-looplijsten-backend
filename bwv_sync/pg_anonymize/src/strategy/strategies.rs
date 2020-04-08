use lipsum::lipsum_words;
use rand::prelude::*;

/// Return a random element from the given slice.
pub(crate) fn element<T>(source: &[T]) -> T
where
    T: Clone,
{
    let mut rng = rand::thread_rng();
    source[rng.gen_range(0, source.len() - 1)].clone()
}

/// Return a single lowercase character in the range a-z.
pub(crate) fn char() -> char {
    let alphabet = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
        's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    ];
    element(&alphabet)
}

/// Return a somewhat random date in the past, compatible with PostgreSQL's timestamp fields.
pub(crate) fn date() -> String {
    let mut rng = rand::thread_rng();
    format!(
        "{year}-{month:02}-{day:02} 00:00:00",
        year = rng.gen_range(1940, 2019),
        month = rng.gen_range(1, 12),
        day = rng.gen_range(1, 28)
    )
}

/// Return a random name from `data/given_names.txt`.
pub(crate) fn given_name() -> &'static str {
    const NAMES: &'static [&str] = include!(concat!(env!("OUT_DIR"), "/given_names.rs"));
    const NAMES_LEN: usize = NAMES.len();

    let mut rng = rand::thread_rng();
    let index = rng.gen_range(0, NAMES_LEN - 1);
    NAMES[index]
}

/// Return a random name from `data/surnames.txt`.
pub(crate) fn surname() -> &'static str {
    const NAMES: &'static [&str] = include!(concat!(env!("OUT_DIR"), "/surnames.rs"));
    const NAMES_LEN: usize = NAMES.len();

    let mut rng = rand::thread_rng();
    let index = rng.gen_range(0, NAMES_LEN - 1);
    NAMES[index]
}

/// Generate a somewhat latin paragraph.
pub(crate) fn prose(length: usize) -> String {
    let mut rng = rand::thread_rng();
    let no_words = rng.gen_range(5, 50);
    lipsum_words(no_words).chars().take(length).collect()
}

/// Generate a random (semi-) phone number.
pub(crate) fn phone_nr() -> String {
    let mut rng = rand::thread_rng();
    let nr: u64 = rng.gen_range(1000000000, 9999999999);
    format!("{}", nr)
}

/// Generate a melding
pub(crate) fn melding(toezichthouder_codes: &Vec<String>) -> String {
    let mut rng = rand::thread_rng();
    let date = format!(
        "{}-{}-{}",
        rng.gen_range(1, 28),
        element(&["JAN", "FEB", "MAR", "APR", "MEI", "JUN", "JUL", "SEP", "OKT", "NOV", "DEC"]),
        rng.gen_range(10, 20)
    );
    let no_words = rng.gen_range(5, 20);
    let content = format!(
        "{}({}): {}",
        element(&toezichthouder_codes),
        date,
        lipsum_words(no_words)
    );

    if rand::random() {
        format!("{}\\n{}", content, melding(toezichthouder_codes))
    } else {
        content.chars().take(1800).collect()
    }
}
