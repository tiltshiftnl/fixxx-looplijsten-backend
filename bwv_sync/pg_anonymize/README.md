# pg_anonymize

Anonymize PostgreSQL tables, e.g. for production-like data in development
environments.

`pg_anonymize` takes the output of the PostgreSQL `COPY` command and replaces
the values of columns according to your configuration. This makes it convenient
to anonymize data on-the-fly while importing from another database, as well as
making an anonymized copy of a table in the same database.

Because `pg_anonymize` works on the output of the `COPY` command we
unfortunately cannot act on fields in other tables than the one we're currently
processing. **This means we cannot dynamically anonymize foreign keys.** For
some use cases a workaround might be to instead use the `OneOf` strategy with a
list of hard coded valid values.

## Examples

```bash
psql -c 'COPY <table_name> TO STDOUT' |
  pg_anonymize -c config.yaml <table_name> |
  psql -c 'COPY <table_name> from STDIN'
```

where `config.yaml` looks as follows:

```yaml
tables:
  <table_name>:
    some_private_column:
      # `some_private_column` is the nth column (starting at 0). This order is
      # the same as the order in the *psql* output of `\d some_private_column`.
      order: 1
      # The kind of data to fill this column with.
      strategy: Name
    primary_colors:
      order: 2
      strategy:
        OneOf:
          - red
          - green
          - blue
```

## Configuration

Configuration is done through a yaml file that contains a mapping from columns
to strategies. A strategy determines the kind of values that can be generated
for the given column.

Currently implemented strategies are:
* *Date*: Somewhat random date in the last few decades
* *Characters*: One or more uppercase characters in the range A-Z
* *Name*: A full name, created by combining a given name and surname from
  `data/given_names.txt` and `data/surname.txt`
* *Prose*: A paragraph (semi-) Lorem Ipsum
* *PhoneNr*: A random 10-digit number
* *OneOf*: Returns an item from a given list

I'm planning on making these strategies more flexible in the future. Let me
know if there is any interest :).

## Building

### In docker

`docker build -t pg_anonymize .`

### Local

`cargo build --release`

If you haven't got rust/cargo installed on your system yet, I suggest
[rustup](https://rustup.rs/).
