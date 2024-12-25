type KeyOrLock = Vec<i32>;

const KEY_WIDTH: usize = 5;
const KEY_HEIGHT: i32 = 5;

fn parse_input(input_str: &str) -> (Vec<KeyOrLock>, Vec<KeyOrLock>) {
    let blocks: Vec<&str> = input_str.split("\n\n").collect();
    let mut keys: Vec<KeyOrLock> = Vec::new();
    let mut locks: Vec<KeyOrLock> = Vec::new();

    for block in blocks {
        let mut current = vec![-1; KEY_WIDTH];
        let is_key = block.chars().next().unwrap_or(' ') == '#';

        for (y, line) in block.lines().enumerate() {
            for (x, c) in line.chars().enumerate() {
                if is_key && c == '.' && current[x] == -1 {
                    current[x] = y as i32 - 1;
                }
                if !is_key && c == '.' {
                    current[x] = KEY_HEIGHT - y as i32;
                }
            }
        }

        if is_key {
            keys.push(current);
        } else {
            locks.push(current);
        }
    }

    (keys, locks)
}

fn does_fit(key: &KeyOrLock, lock: &KeyOrLock) -> bool {
    key.iter()
        .zip(lock.iter())
        .all(|(k, l)| k + l <= KEY_HEIGHT)
}

fn part_1(keys: &[KeyOrLock], locks: &[KeyOrLock]) -> usize {
    keys.iter()
        .flat_map(|key| locks.iter().map(move |lock| does_fit(key, lock)))
        .filter(|&fits| fits)
        .count()
}

fn main() {
    let input = include_str!("../../../inputs/input_25.txt");
    let (keys, locks) = parse_input(input);
    println!("Part 1: {}", part_1(&keys, &locks));
}
