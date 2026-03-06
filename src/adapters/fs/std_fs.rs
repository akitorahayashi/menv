//! Standard filesystem adapter — thin wrapper around `std::fs`.

use std::path::{Path, PathBuf};

use crate::domain::error::AppError;
use crate::domain::ports::fs::FsPort;

pub struct StdFs;

impl FsPort for StdFs {
    fn exists(&self, path: &Path) -> bool {
        path.exists()
    }

    fn read_to_string(&self, path: &Path) -> Result<String, AppError> {
        std::fs::read_to_string(path).map_err(AppError::Io)
    }

    fn read_dir(&self, path: &Path) -> Result<Vec<PathBuf>, AppError> {
        std::fs::read_dir(path)
            .map_err(AppError::Io)?
            .map(|entry| entry.map(|e| e.path()).map_err(AppError::Io))
            .collect()
    }

    fn write(&self, path: &Path, content: &[u8]) -> Result<(), AppError> {
        std::fs::write(path, content).map_err(AppError::Io)
    }

    fn create_dir_all(&self, path: &Path) -> Result<(), AppError> {
        std::fs::create_dir_all(path).map_err(AppError::Io)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::tempdir;

    #[test]
    fn std_fs_exists() {
        let fs = StdFs;
        let dir = tempdir().unwrap();
        let file_path = dir.path().join("test.txt");

        assert!(!fs.exists(&file_path));
        std::fs::write(&file_path, "test").unwrap();
        assert!(fs.exists(&file_path));
    }

    #[test]
    fn std_fs_read_write() {
        let fs = StdFs;
        let dir = tempdir().unwrap();
        let file_path = dir.path().join("test.txt");

        fs.write(&file_path, b"hello").unwrap();
        assert_eq!(fs.read_to_string(&file_path).unwrap(), "hello");
    }

    #[test]
    fn std_fs_read_dir() {
        let fs = StdFs;
        let dir = tempdir().unwrap();
        let file_path1 = dir.path().join("1.txt");
        let file_path2 = dir.path().join("2.txt");

        fs.write(&file_path1, b"1").unwrap();
        fs.write(&file_path2, b"2").unwrap();

        let mut entries = fs.read_dir(dir.path()).unwrap();
        entries.sort();

        assert_eq!(entries.len(), 2);
        assert_eq!(entries[0], file_path1);
        assert_eq!(entries[1], file_path2);
    }

    #[test]
    fn std_fs_create_dir_all() {
        let fs = StdFs;
        let dir = tempdir().unwrap();
        let deep_dir = dir.path().join("a").join("b").join("c");

        assert!(!fs.exists(&deep_dir));
        fs.create_dir_all(&deep_dir).unwrap();
        assert!(fs.exists(&deep_dir));
        assert!(deep_dir.is_dir());
    }
}
