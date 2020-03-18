use serde::Deserialize;
use structopt::StructOpt;

use std::collections::HashMap;
use std::io::BufRead;
use std::path::PathBuf;

mod strategy;
use strategy::Strategy;

fn main() {
    let opts = Opts::from_args();
    let config_raw = std::fs::read_to_string(&opts.config).expect("Failed to read config file");
    let config: Config = serde_yaml::from_str(&config_raw).expect("Failed to decode config file");
    let stdin = std::io::stdin();

    for row in stdin.lock().lines() {
        let row = row.unwrap();
        process_row(&config.tables, &row, &opts.table);
    }
}

fn process_row<'a>(config: &HashMap<TableName, TableConfig>, row: &'a str, table: &str) {
    // If we don't have a translation config for a table, we just print the row unchanged.
    let table_config = match config.get(table) {
        Some(config) => config,
        None => {
            println!("{}", row);
            return;
        }
    };

    let mut new_row: Vec<String> = row.split('\t').map(|s| s.to_string()).collect();
    for (_column_name, config) in table_config {
        if config.column >= new_row.len() {
            panic!("Column {} does not exist in {}", config.column, table);
        }
        let new_value = config.strategy.generate();
        new_row[config.column] = new_value;
    }
    println!("{}", new_row.join("\t"));
}

/// `Opts` contains the command line arguments passed to our program.
#[derive(Debug, StructOpt)]
#[structopt(name = "pg_anonymize", about = "Anonymize PostgreSQL COPY output")]
struct Opts {
    #[structopt()]
    /// The table we're COPY-ing
    table: String,
    #[structopt(short = "c", long = "config", parse(from_os_str))]
    config: PathBuf,
}

type TableName = String;

/// `Config` represents our configuration file.
#[derive(Deserialize)]
struct Config {
    /// tables contains the configuration for our tables, indexed by TableName.
    tables: HashMap<TableName, TableConfig>,
}

type ColumnName = String;
type TableConfig = HashMap<ColumnName, ColumnConfig>;

/// `ColumnConfig` represents the actual anonymization configuration for a column.
#[derive(Deserialize)]
struct ColumnConfig {
    /// `column` is used to identify the column. Unfortunately we can't match on name; instead we
    /// need to know the index (relative order) of the column relative to the other columns.
    column: usize,
    /// `Strategy` determines the strategy used to generate data for this column.
    strategy: Strategy,
}
