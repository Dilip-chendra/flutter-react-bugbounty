import os
import shutil
import random
from typing import List, Optional
import logging

class SecureDataWiper:
    def __init__(self, app_data_paths: List[str]):
        """Initialize with paths to app data locations."""
        self.app_data_paths = app_data_paths
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for the data wiping process."""
        logger = logging.getLogger('SecureDataWiper')
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    def secure_wipe_file(self, file_path: str, passes: int = 3) -> bool:
        """Securely wipe a file using multiple overwrite passes."""
        try:
            if not os.path.exists(file_path):
                return False
                
            file_size = os.path.getsize(file_path)
            
            with open(file_path, 'wb') as f:
                for pass_num in range(passes):
                    # Seek to beginning of file
                    f.seek(0)
                    
                    # Different patterns for each pass
                    if pass_num == 0:
                        # First pass: all zeros
                        pattern = b'\x00'
                    elif pass_num == 1:
                        # Second pass: all ones
                        pattern = b'\xFF'
                    else:
                        # Third pass: random data
                        pattern = bytes([random.randint(0, 255)])
                    
                    # Write pattern
                    for _ in range(0, file_size, 4096):
                        f.write(pattern * min(4096, file_size - _))
                    
                    # Flush to disk
                    f.flush()
                    os.fsync(f.fileno())
                    
            # Finally, delete the file
            os.remove(file_path)
            self.logger.info(f"Successfully wiped file: {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error wiping file {file_path}: {str(e)}")
            return False
    
    def secure_wipe_directory(self, directory: str, passes: int = 3) -> bool:
        """Recursively wipe all files in a directory."""
        try:
            if not os.path.exists(directory):
                return False
                
            # First, wipe all files
            for root, dirs, files in os.walk(directory, topdown=False):
                for name in files:
                    file_path = os.path.join(root, name)
                    self.secure_wipe_file(file_path, passes)
                    
            # Then remove empty directories
            shutil.rmtree(directory)
            self.logger.info(f"Successfully wiped directory: {directory}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error wiping directory {directory}: {str(e)}")
            return False
    
    def wipe_app_data(self, additional_paths: Optional[List[str]] = None) -> dict:
        """Wipe all app data from specified locations."""
        results = {'success': [], 'failed': []}
        
        # Combine default and additional paths
        paths_to_wipe = self.app_data_paths.copy()
        if additional_paths:
            paths_to_wipe.extend(additional_paths)
            
        for path in paths_to_wipe:
            if os.path.isfile(path):
                success = self.secure_wipe_file(path)
            elif os.path.isdir(path):
                success = self.secure_wipe_directory(path)
            else:
                success = False
                
            if success:
                results['success'].append(path)
            else:
                results['failed'].append(path)
                
        return results
    
    def verify_data_removal(self, paths: List[str]) -> bool:
        """Verify that all specified paths have been removed."""
        for path in paths:
            if os.path.exists(path):
                self.logger.error(f"Data still exists at: {path}")
                return False
        return True

# Usage example:
if __name__ == "__main__":
    # Example app data paths
    app_paths = [
        "./app_data",
        "./user_preferences.json",
        "./cache"
    ]
    
    # Initialize wiper
    wiper = SecureDataWiper(app_paths)
    
    # Additional paths to wipe
    additional_paths = [
        "./downloads",
        "./temp"
    ]
    
    # Wipe all data
    results = wiper.wipe_app_data(additional_paths)
    
    # Print results
    print("Successfully wiped:", results['success'])
    print("Failed to wipe:", results['failed'])
    
    # Verify removal
    all_paths = app_paths + additional_paths
    if wiper.verify_data_removal(all_paths):
        print("All data successfully removed")
    else:
        print("Some data may still remain") 