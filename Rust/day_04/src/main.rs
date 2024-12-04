fn parse_input(input: &str) -> Vec<Vec<char>> {
    input.lines().map(|line| line.chars().collect()).collect()
}

fn part_1(grid: &[Vec<char>]) -> usize {
    let to_find = "XMAS".to_string();
    let l = to_find.len();
    let mut cnt = 0;
    for y in 0..grid.len() {
        for x in 0..grid[0].len() {
            // horizontal
            if x + l <= grid[0].len()
                && to_find == (0..l).map(|i| grid[y][x + i]).collect::<String>()
            {
                cnt += 1;
            }
            if x + 1 >= l && (0..l).map(|i| grid[y][x - i]).collect::<String>() == to_find {
                cnt += 1;
            }
            // vertical
            if y + l <= grid.len() && (0..l).map(|i| grid[y + i][x]).collect::<String>() == to_find
            {
                cnt += 1;
            }
            if y + 1 >= l && (0..l).map(|i| grid[y - i][x]).collect::<String>() == to_find {
                cnt += 1;
            }

            // diagonal
            if y + l <= grid.len()
                && x + l <= grid.len()
                && (0..l).map(|i| grid[y + i][x + i]).collect::<String>() == to_find
            {
                cnt += 1;
            }
            if y + 1 >= l
                && x + l <= grid.len()
                && (0..l).map(|i| grid[y - i][x + i]).collect::<String>() == to_find
            {
                cnt += 1;
            }
            if y + l <= grid.len()
                && x + 1 >= l
                && (0..l).map(|i| grid[y + i][x - i]).collect::<String>() == to_find
            {
                cnt += 1;
            }
            if y + 1 >= l
                && x + 1 >= l
                && (0..l).map(|i| grid[y - i][x - i]).collect::<String>() == to_find
            {
                cnt += 1;
            }
        }
        //  println!();
    }
    cnt
}
fn part_2(grid: &[Vec<char>]) -> i32 {
    let to_find = "MAS";
    let l = to_find.len();
    let mut cnt = 0;
    for y in 0..=(grid.len() - l) {
        for x in 0..=(grid[0].len() - l) {
            let diag1: String = (0..l).map(|i| grid[y + i][x + i]).collect();
            let diag2: String = (0..l).map(|i| grid[y + i][x + l - 1 - i]).collect();

            if (diag1 == to_find || diag1.chars().rev().collect::<String>() == to_find)
                && (diag2 == to_find || diag2.chars().rev().collect::<String>() == to_find)
            {
                cnt += 1;
            }
        }
    }

    cnt
}

fn main() {
    let input = include_str!("../../../inputs/input_04.txt");
    let grid = parse_input(input);
    println!("Part 1: {}", part_1(&grid));
    println!("Part 2: {}", part_2(&grid));
}
