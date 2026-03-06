//! Filesystem port — interface for file system operations.

use crate::domain::error::AppError;

/// Provides file system operations.
pub trait FsPort {
    /// Check whether a path exists.
    fn exists(&self, path: &str) -> bool;

    /// Read a file to a string.
    fn read_to_string(&self, path: &str) -> Result<String, AppError>;

    /// List entries in a directory.
    fn read_dir(&self, path: &str) -> Result<Vec<String>, AppError>;

    /// Write content to a file.
    fn write(&self, path: &str, content: &[u8]) -> Result<(), AppError>;

    /// Create a directory and all parent directories.
    fn create_dir_all(&self, path: &str) -> Result<(), AppError>;
}
