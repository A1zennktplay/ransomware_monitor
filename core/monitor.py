import hashlib
import os
import json
import time
from datetime import datetime
from pathlib import Path
import threading


class FileIntegrityMonitor:
    def __init__(self):
        self.directory = None
        self.baseline_file = Path("baseline.json")
        self.baseline = {}
        self.alerts = []
        self.stats = {
            'total': 0,
            'unchanged': 0,
            'modified': 0,
            'deleted': 0,
            'new': 0
        }
        self.is_monitoring = False
        self.monitor_thread = None
        self.scan_interval = 5
        self.files_list = []
    
    def set_directory(self, directory):
        """Set the directory to monitor"""
        self.directory = Path(directory)
        if not self.directory.exists():
            raise ValueError(f"Directory does not exist: {directory}")
        return True
    
    def generate_hash(self, filepath):
        """Generate SHA-256 hash for a file"""
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            print(f"Error hashing file {filepath}: {e}")
            return None
    
    def create_baseline(self):
        """Create baseline hashes for all files"""
        if not self.directory:
            return False
        
        self.baseline = {}
        file_count = 0
        
        for root, dirs, files in os.walk(self.directory):
            for filename in files:
                filepath = Path(root) / filename
                try:
                    file_hash = self.generate_hash(filepath)
                    if file_hash:
                        file_stats = filepath.stat()
                        self.baseline[str(filepath)] = {
                            'hash': file_hash,
                            'size': file_stats.st_size,
                            'modified': file_stats.st_mtime,
                            'path': str(filepath),
                            'name': filename
                        }
                        file_count += 1
                except Exception as e:
                    print(f"Error processing {filepath}: {e}")
        
        self.save_baseline()
        self.add_alert('success', f'Baseline created for {file_count} files')
        return True
    
    def save_baseline(self):
        """Save baseline to JSON file"""
        try:
            with open(self.baseline_file, 'w') as f:
                json.dump(self.baseline, f, indent=2)
        except Exception as e:
            print(f"Error saving baseline: {e}")
    
    def load_baseline(self):
        """Load baseline from JSON file"""
        if not self.baseline_file.exists():
            return False
        try:
            with open(self.baseline_file, 'r') as f:
                self.baseline = json.load(f)
            return True
        except Exception as e:
            print(f"Error loading baseline: {e}")
            return False
    
    def add_alert(self, alert_type, message, filepath=""):
        """Add an alert"""
        alert = {
            'type': alert_type,
            'message': message,
            'filepath': filepath,
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'id': time.time()
        }
        self.alerts.insert(0, alert)
        if len(self.alerts) > 50:
            self.alerts = self.alerts[:50]
    
    def scan_files(self):
        """Scan all files and compare with baseline"""
        if not self.directory or not self.baseline:
            return False
        
        current_files = set()
        self.files_list = []
        
        self.stats = {
            'total': 0,
            'unchanged': 0,
            'modified': 0,
            'deleted': 0,
            'new': 0
        }
        
        # Scan current files
        for root, dirs, files in os.walk(self.directory):
            for filename in files:
                filepath = Path(root) / filename
                filepath_str = str(filepath)
                current_files.add(filepath_str)
                
                self.stats['total'] += 1
                
                file_info = {
                    'name': filename,
                    'path': str(filepath.parent),
                    'full_path': filepath_str,
                    'status': 'unchanged',
                    'hash': '',
                    'size': 0
                }
                
                # Check if file is in baseline
                if filepath_str not in self.baseline:
                    file_info['status'] = 'new'
                    self.stats['new'] += 1
                    self.add_alert('warning', 'New file detected', filepath_str)
                else:
                    # Calculate current hash
                    current_hash = self.generate_hash(filepath)
                    baseline_hash = self.baseline[filepath_str]['hash']
                    
                    file_info['hash'] = current_hash[:16] + '...'
                    file_info['size'] = filepath.stat().st_size
                    
                    if current_hash != baseline_hash:
                        file_info['status'] = 'modified'
                        self.stats['modified'] += 1
                        self.add_alert('danger', 'FILE MODIFIED - Possible ransomware!', filepath_str)
                    else:
                        file_info['status'] = 'unchanged'
                        self.stats['unchanged'] += 1
                
                self.files_list.append(file_info)
        
        # Check for deleted files
        baseline_files = set(self.baseline.keys())
        deleted_files = baseline_files - current_files
        
        for deleted_file in deleted_files:
            self.stats['deleted'] += 1
            file_info = {
                'name': Path(deleted_file).name,
                'path': str(Path(deleted_file).parent),
                'full_path': deleted_file,
                'status': 'deleted',
                'hash': self.baseline[deleted_file]['hash'][:16] + '...',
                'size': self.baseline[deleted_file]['size']
            }
            self.files_list.append(file_info)
            self.add_alert('danger', 'FILE DELETED - Possible ransomware!', deleted_file)
        
        return True
    
    def start_monitoring(self):
        """Start continuous monitoring"""
        if self.is_monitoring:
            return False
        
        self.is_monitoring = True
        self.add_alert('info', 'Real-time monitoring started')
        
        def monitor_loop():
            while self.is_monitoring:
                self.scan_files()
                time.sleep(self.scan_interval)
        
        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
        return True
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.is_monitoring = False
        self.add_alert('info', 'Monitoring stopped')
        return True