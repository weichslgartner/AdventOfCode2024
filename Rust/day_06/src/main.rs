use std::collections::HashSet;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct Point {
    x: i32,
    y: i32,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
enum Direction {
    North,
    East,
    South,
    West,
}

impl Direction {
    fn next(self) -> Self {
        match self {
            Direction::North => Direction::East,
            Direction::East => Direction::South,
            Direction::South => Direction::West,
            Direction::West => Direction::North,
        }
    }

    fn to_point(self) -> Point {
        match self {
            Direction::North => Point { x: 0, y: -1 },
            Direction::East => Point { x: 1, y: 0 },
            Direction::South => Point { x: 0, y: 1 },
            Direction::West => Point { x: -1, y: 0 },
        }
    }
}

fn parse_input(lines: Vec<&str>) -> (HashSet<Point>, Point, Point) {
    let mut obstacles = HashSet::new();
    let mut start = None;

    for (y, line) in lines.iter().enumerate() {
        for (x, c) in line.chars().enumerate() {
            let point = Point {
                x: x as i32,
                y: y as i32,
            };

            match c {
                '#' => {
                    obstacles.insert(point);
                }
                '^' => {
                    start = Some(point);
                }
                _ => {}
            }
        }
    }

    (
        obstacles,
        start.unwrap(),
        Point {
            x: lines[0].len() as i32,
            y: lines.len() as i32,
        },
    )
}

fn part_1(obstacles: &HashSet<Point>, start: Point, max_p: Point) -> usize {
    let mut cur = start;
    let mut visited = HashSet::new();
    let mut dir = Direction::North;

    while cur.x >= 0 && cur.x < max_p.x && cur.y >= 0 && cur.y < max_p.y {
        let mut next = dir.to_point();
        let mut next_p = Point {
            x: cur.x + next.x,
            y: cur.y + next.y,
        };

        while obstacles.contains(&next_p) {
            dir = dir.next();
            next = dir.to_point();
            next_p = Point {
                x: cur.x + next.x,
                y: cur.y + next.y,
            };
        }

        visited.insert(cur);
        cur = next_p;
    }

    visited.len()
}

fn part_2(obstacles: &mut HashSet<Point>, start: Point, max_p: Point) -> usize {
    let mut cur = start;
    let mut visited_dir = HashSet::new();
    let mut new_obstacles = HashSet::new();
    let mut dir = Direction::North;
    let mut cnt = 0;
    while cur.x >= 0 && cur.x < max_p.x && cur.y >= 0 && cur.y < max_p.y {
        let (new_dir, next_p) = get_next_point(cur, dir, obstacles);
        if !obstacles.contains(&next_p) && !new_obstacles.contains(&next_p) {
            obstacles.insert(next_p);

            if has_loops(cur, dir, max_p, obstacles, &visited_dir) {
                new_obstacles.insert(next_p);
            }

            
            obstacles.remove(&next_p);
        }
        visited_dir.insert((cur, dir));
        cur = next_p;
        dir = new_dir;
    }

    new_obstacles.len()
}

fn has_loops(
    mut cur: Point,
    mut dir: Direction,
    max_p: Point,
    obstacles: &HashSet<Point>,
    visited_dir_: &HashSet<(Point, Direction)>,
) -> bool {
    let max_search = 9_000_000;
    let mut visited_dir = visited_dir_.clone();
    let mut i = 0;
    while cur.x >= 0 && cur.x < max_p.x && cur.y >= 0 && cur.y < max_p.y && i < max_search {
        if visited_dir.contains(&(cur, dir)) {
            return true;
        }
       visited_dir.insert((cur, dir));

        let (new_dir, next_p) = get_next_point(cur, dir, obstacles);

        cur = next_p;
        dir = new_dir;
        i += 1;
    }

    false
}

fn get_next_point(
    cur: Point,
    mut dir: Direction,
    obstacles: &HashSet<Point>,
) -> (Direction, Point) {
    let mut next = dir.to_point();
    let mut next_p = Point {
        x: cur.x + next.x,
        y: cur.y + next.y,
    };

    while obstacles.contains(&next_p) {
        dir = dir.next();
        next = dir.to_point();
        next_p = Point {
            x: cur.x + next.x,
            y: cur.y + next.y,
        };
    }

    (dir, next_p)
}

fn main() {
    let input = include_str!("../../../inputs/input_06.txt");
    let lines: Vec<&str> = input.lines().collect();

    let (mut obstacles, start, max_p) = parse_input(lines);

    println!("Part 1: {}", part_1(&obstacles, start, max_p));
    println!("Part 2: {}", part_2(&mut obstacles, start, max_p));
}
