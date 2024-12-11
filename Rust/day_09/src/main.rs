use itertools::Itertools;
use std::collections::HashMap;

fn parse_input(disk_map: &str) -> (Vec<isize>, HashMap<usize, usize>, HashMap<usize, usize>) {
    let mut block_id = 0;
    let mut res = Vec::new();
    let mut is_id = true;
    let mut free_space = HashMap::new();
    let mut blocks = HashMap::new();

    for c in disk_map.trim().chars() {
        let count = c.to_digit(10).unwrap() as usize;
        if is_id {
            blocks.insert(res.len(), count);
            for _ in 0..count {
                res.push(block_id);
            }
            block_id += 1;
        } else {
            free_space.insert(res.len(), count);
            for _ in 0..count {
                res.push(-1);
            }
        }
        is_id = !is_id;
    }
    (res, free_space, blocks)
}

fn checksum(disk: &[isize]) -> usize {
    disk.iter()
        .enumerate()
        .filter_map(|(i, c)| if *c >= 0 { Some(i * *c as usize) } else { None })
        .sum()
}

fn part_1(mut disk_map: Vec<isize>) -> usize {
    let mut left = disk_map.iter().position(|c| *c == -1).unwrap();
    let mut right = disk_map.len() - 1;
    while left <= right {
        disk_map.swap(left, right);
        left = disk_map
            .iter()
            .skip(left + 1)
            .position(|c| *c == -1)
            .unwrap_or(disk_map.len())
            + left
            + 1;
        while right > 0 && disk_map[right] == -1 {
            right -= 1;
        }
    }
    checksum(&disk_map)
}

fn find_target(
    free_space: &HashMap<usize, usize>,
    idx: usize,
    keys: &[usize],
    length: usize,
) -> Option<usize> {
    for (target, &key) in keys.iter().enumerate() {
        if let Some(&space) = free_space.get(&key) {
            if length <= space {
                if idx > key {
                    return Some(target);
                }
                return None;
            }
        }
    }
    None
}

fn part_2(
    mut disk_map: Vec<isize>,
    mut free_space: HashMap<usize, usize>,
    blocks: HashMap<usize, usize>,
) -> usize {
    let mut keys: Vec<usize> = free_space.keys().cloned().sorted().collect();
    for (idx, length) in blocks.iter().sorted().rev() {
        if let Some(target) = find_target(&free_space, *idx, &keys, *length) {
            let key = keys[target];
            {
                let s = key + length;
                let (left, right) = disk_map.split_at_mut(s);
                left[key..key + length].swap_with_slice(&mut right[idx - s..idx + length - s]);
            }
            if let Some(&space) = free_space.get(&key) {
                if space > *length {
                    free_space.insert(key + length, space - length);
                    keys[target] = key + length;
                } else {
                    keys.remove(target);
                }
            }
        }
    }
    checksum(&disk_map)
}

fn main() {
    let input = include_str!("../../../inputs/input_09.txt");
    let (disk_map, free_space, blocks) = parse_input(&input);
    println!("Part 1: {}", part_1(disk_map.clone()));
    println!("Part 2: {}", part_2(disk_map, free_space, blocks));
}
