use anyhow::Result;
use std::str::FromStr;

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
        .map(|line| line_to_int::<T,SPLIT_CHAR>(line))
        .collect()
}
