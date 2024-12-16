use anyhow::Result;
use regex::Regex;
use std::{collections::HashSet, str::FromStr};

/// Parses a line of text into a vector of values of type `T`, splitting by `SPLIT_CHAR`.
///
/// # Arguments
/// * `line` - A string slice containing the input line to parse.
///
/// # Returns
/// A `Result` containing a vector of parsed values, or an error if parsing fails for any element.
///
/// # Examples
///
/// ```
/// use aoc::line_to_int;
///
/// let result: Result<Vec<i32>, _> = line_to_int::<i32, ','>("1,2,3");
/// assert_eq!(result, Ok(vec![1, 2, 3]));
///
/// let result: Result<Vec<i32>, _> = line_to_int::<i32, ','>("4, 5, 6");
/// assert!(result.is_err()); // Whitespace would cause parsing to fail.
///
/// let result: Result<Vec<i32>, _> = line_to_int::<i32, ','>("");
/// assert_eq!(result, Ok(vec![])); // Empty input gives an empty vector.
/// ```
pub fn line_to_int<T: FromStr, const SPLIT_CHAR: char>(line: &str) -> Result<Vec<T>, T::Err> {
    line.split(SPLIT_CHAR)
        .filter(|i| !i.is_empty())
        .map(|i| i.parse::<T>())
        .collect()
}

/// Parses multiple lines of text into a vector of vectors of values of type `T`, splitting each line by `SPLIT_CHAR`.
///
/// # Arguments
/// * `input` - A string slice containing the input with multiple lines to parse.
///
/// # Returns
/// A `Result` containing a vector of vectors of parsed values, or an error if parsing fails for any element.
///
/// # Examples
///
/// ```
/// use aoc::parse_ints;
///
/// let input = "1,2,3\n4,5,6";
/// let result: Result<Vec<Vec<i32>>, _> = parse_ints::<i32, ','>(input);
/// assert_eq!(result, Ok(vec![vec![1, 2, 3], vec![4, 5, 6]]));
///
/// let input = "7 8\n9  10";
/// let result: Result<Vec<Vec<i32>>, _> = parse_ints::<i32, ' '>(input);
/// assert_eq!(result, Ok(vec![vec![7, 8], vec![9, 10]]));
///
/// let input = "11,12\ninvalid,13";
/// let result: Result<Vec<Vec<i32>>, _> = parse_ints::<i32, ','>(input);
/// assert!(result.is_err()); // Parsing fails due to "invalid".
/// ```
pub fn parse_ints<T: FromStr, const SPLIT_CHAR: char>(input: &str) -> Result<Vec<Vec<T>>, T::Err> {
    input
        .lines()
        .map(|line| line_to_int::<T, SPLIT_CHAR>(line))
        .collect()
}

/// A structure representing a point in a 2D grid.
///
/// # Fields
/// - `x`: The x-coordinate of the point.
/// - `y`: The y-coordinate of the point.
#[derive(Debug, PartialEq, Eq, Ord,PartialOrd, Clone, Copy, Hash)]
pub struct Point {
    pub x: isize,
    pub y: isize,
}

impl Point {
    /// Creates a new `Point` with the given x and y coordinates.
    ///
    /// # Arguments
    /// - `x`: The x-coordinate of the point.
    /// - `y`: The y-coordinate of the point.
    ///
    /// # Examples
    /// ```
    /// use aoc::Point;
    ///
    /// let p = Point::new(3, 5);
    /// assert_eq!(p.x, 3);
    /// assert_eq!(p.y, 5);
    /// ```
    pub fn new(x: isize, y: isize) -> Self {
        Self { x, y }
    }
}

/// Checks if a given point `p` lies within the bounds of a grid defined by the maximum point `p_max`.
///
/// # Arguments
/// - `p`: The point to check.
/// - `p_max`: The maximum bounds of the grid. Points are valid if `0 <= x < p_max.x` and `0 <= y < p_max.y`.
///
/// # Returns
/// - `true` if the point is within the grid bounds.
/// - `false` otherwise.
///
/// # Examples
/// ```
/// use aoc::{Point, is_in_grid};
///
/// let p = Point::new(2, 3);
/// let grid_max = Point::new(5, 5);
/// assert!(is_in_grid(p, grid_max));
///
/// let outside_p = Point::new(5, 3);
/// assert!(!is_in_grid(outside_p, grid_max));
/// ```
pub fn is_in_grid(p: Point, p_max: Point) -> bool {
    p.x >= 0 && p.y >= 0 && p.x < p_max.x && p.y < p_max.y
}

/// Returns the 4-connected neighbors of a given point within a defined maximum boundary.
///
/// The neighbors are the points directly adjacent to the input point (up, down, left, and right),
/// constrained by the boundaries defined by `p_max`.
///
/// # Examples
///
/// ```
/// use aoc::{Point, get_neighbours_4};
///
/// let point = Point { x: 1, y: 1 };
/// let boundary = Point { x: 3, y: 3 };
/// let neighbors = get_neighbours_4(point, boundary);
/// assert_eq!(neighbors, vec![
///     Point { x: 0, y: 1 },
///     Point { x: 1, y: 0 },
///     Point { x: 2, y: 1 },
///     Point { x: 1, y: 2 }
/// ]);
///
/// let corner_point = Point { x: 0, y: 0 };
/// let neighbors = get_neighbours_4(corner_point, boundary);
/// assert_eq!(neighbors, vec![
///     Point { x: 1, y: 0 },
///     Point { x: 0, y: 1 }
/// ]);
/// ```
pub fn get_neighbours_4(p: Point, p_max: Point) -> Vec<Point> {
    let mut neighbours = Vec::new();
    if p.x > 0 {
        neighbours.push(Point { x: p.x - 1, y: p.y });
    }
    if p.y > 0 {
        neighbours.push(Point { x: p.x, y: p.y - 1 });
    }
    if p.x + 1 < p_max.x {
        neighbours.push(Point { x: p.x + 1, y: p.y });
    }
    if p.y + 1 < p_max.y {
        neighbours.push(Point { x: p.x, y: p.y + 1 });
    }
    neighbours
}

/// Extracts all integers from a given string.
///
/// This function scans the input string for integers (including negative values) and returns them as a vector.
///
/// # Examples
///
/// ```
/// use aoc::extract_all_ints;
/// use regex::Regex;
///
/// let input = "The temperatures are -12, -5, and 14 degrees.";
/// let result = extract_all_ints(input);
/// assert_eq!(result, vec![-12, -5, 14]);
///
/// let input = "No numbers here!";
/// let result = extract_all_ints(input);
/// assert!(result.is_empty());
///
/// let input = "Mixed 42text and-7numbers33.";
/// let result = extract_all_ints(input);
/// assert_eq!(result, vec![42, -7, 33]);
/// ```
///
/// # Panics
///
/// This function will panic if the regular expression is invalid, but this is unlikely as the regex pattern is hardcoded.
pub fn extract_all_ints(line: &str) -> Vec<isize> {
    let re = Regex::new(r"-?\d+").unwrap();
    re.find_iter(line)
        .filter_map(|mat| mat.as_str().parse::<isize>().ok())
        .collect()
}

#[derive(Debug, PartialEq, Eq, Ord,PartialOrd, Clone, Copy, Hash)]
pub enum Direction {
    North,
    East,
    South,
    West,
}

impl Direction {
    pub fn from_char(c: char) -> Option<Self> {
        match c {
            '^' => Some(Direction::North),
            '>' => Some(Direction::East),
            'v' => Some(Direction::South),
            '<' => Some(Direction::West),
            _ => None,
        }
    }

    pub fn to_point(&self) -> Point {
        match self {
            Direction::North => Point::new(0, -1),
            Direction::East => Point::new(1, 0),
            Direction::South => Point::new(0, 1),
            Direction::West => Point::new(-1, 0),
        }
    }
    pub fn rotate(self, clockwise: bool) -> Self {
        match (self, clockwise) {
            (Direction::North, true) => Direction::East,
            (Direction::East, true) => Direction::South,
            (Direction::South, true) => Direction::West,
            (Direction::West, true) => Direction::North,
            (Direction::North, false) => Direction::West,
            (Direction::West, false) => Direction::South,
            (Direction::South, false) => Direction::East,
            (Direction::East, false) => Direction::North,
        }
    }

    pub fn all() -> Vec<Self> {
        vec![
            Direction::North,
            Direction::East,
            Direction::South,
            Direction::West,
        ]
    }
}


pub fn print_grid(tiles_best_paths: &HashSet<Point>, walls: &HashSet<Point>) {
    let max_x = walls.iter().map(|p| p.x).max().unwrap();
    let max_y = walls.iter().map(|p| p.y).max().unwrap();

    for y in 0..=max_y {
        for x in 0..=max_x {
            let p = Point { x, y };
            if walls.contains(&p) {
                print!("#");
            } else if tiles_best_paths.contains(&p) {
                print!("O");
            } else {
                print!(".");
            }
        }
        println!();
    }
}