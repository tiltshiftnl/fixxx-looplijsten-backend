FROM rust:1.40 as builder
WORKDIR /app
COPY . .
RUN cargo build --release

FROM gcr.io/distroless/cc
copy --from=builder /app/target/release/pg_anonymize /
CMD ["/pg_anonymize"]
