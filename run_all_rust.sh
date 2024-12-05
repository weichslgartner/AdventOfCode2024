#!/bin/bash
pushd .
cd Rust
for file in day_*
do
    echo ${file%/}
    cargo build --release --bin ${file%/}
    time target/release/${file%/}
    printf "\n"
done
popd