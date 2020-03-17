use serde::Deserialize;

mod strategies;

use strategies::*;

#[derive(Deserialize)]
pub(crate) enum Strategy {
    BinaryGender,
    Date,
    Characters,
    Name,
    Prose,
    PhoneNr,
    OneOf(Vec<String>),
}

impl Strategy {
    // Generate a valid and anonymous value for the field.
    pub(crate) fn generate(&self) -> String {
        use Strategy::*;
        match self {
            BinaryGender => if rand::random() { "M".to_string() } else { "V".to_string() },
            Date => date(),
            Characters => {
                let mut initials = String::new();
                loop {
                    let c = char().to_ascii_uppercase();
                    initials.push(c);
                    if rand::random() {
                        break;
                    }
                }
                initials
            },
            Name => format!("{} {}", given_name(), surname()),
            Prose => prose(),
            PhoneNr => phone_nr(),
            OneOf(list) => element(list),
        }
    }
}
