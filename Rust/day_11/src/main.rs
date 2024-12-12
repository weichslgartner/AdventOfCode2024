use cached::proc_macro::cached;

fn parse_input(input_str: &str) -> Vec<i64> {
    input_str
        .split_whitespace()
        .filter_map(|token| token.parse::<i64>().ok())
        .collect()
}

fn transform_stone(i: i64) -> Vec<i64> {
    if i == 0 {
        return vec![1];
    }
    let length = i.ilog10() + 1;
    if length % 2 == 0 {
        let half_pow = 10_i64.pow(length / 2);
        vec![i / half_pow, i % half_pow]
    } else {
        vec![i * 2024]
    }
}

#[cached]
fn convert_number(num: i64, times: i64) -> i64 {
    if times == 0 {
        return 1;
    }
    transform_stone(num)
        .iter()
        .map(|&i| convert_number(i, times - 1))
        .sum()
}

fn solve(nums: &[i64], n_iter: i64) -> i64 {
    nums.iter().map(|&n| convert_number(n, n_iter)).sum()
}

fn part_1(nums: &[i64]) -> i64 {
    solve(nums, 25)
}

fn part_2(nums: &[i64]) -> i64 {
    solve(nums, 75)
}

fn main() {
    let input = include_str!("../../../inputs/input_11.txt");
    let nums = parse_input(input);
    println!("Part 1: {}", part_1(&nums));
    println!("Part 2: {}", part_2(&nums));
}
