use serde::Deserialize;

mod strategies;

use strategies::*;

#[derive(Deserialize)]
pub(crate) enum Strategy {
    BinaryGender,
    Date,
    Characters(usize),
    Name(usize),
    Prose(usize),
    PhoneNr,
    OneOf(Vec<String>),
}

impl Strategy {
    // Generate a valid and anonymous value for the field.
    pub(crate) fn generate(&self) -> String {
        use Strategy::*;
        match self {
            BinaryGender => {
                if rand::random() {
                    "M".to_string()
                } else {
                    "V".to_string()
                }
            }
            Date => date(),
            Characters(n) => {
                let mut initials = String::new();
                loop {
                    let c = char().to_ascii_uppercase();
                    initials.push(c);
                    if rand::random() {
                        break;
                    }
                    if initials.len() > *n {
                        break;
                    }
                }
                initials
            }
            Name(n) => format!("{} {}", given_name(), surname())
                .chars()
                .take(*n)
                .collect(),
            Prose(n) => prose(*n),
            PhoneNr => phone_nr(),
            OneOf(list) => element(list),
        }
    }
}
