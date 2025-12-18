"""
Anti-Ransomware File Integrity Monitor - Web Dashboard
Flask-based web application with real-time monitoring
"""
from flask import Flask, render_template, jsonify, request
from core.monitor import FileIntegrityMonitor

app = Flask(__name__)
"""
Anti-Ransomware File Integrity Monitor - Web Dashboard
Flask-based web application with real-time monitoring and logging
"""
from flask import Flask, render_template, jsonify, request
from core.monitor import FileIntegrityMonitor
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Global monitor instance
monitor = FileIntegrityMonitor()

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/set-directory', methods=['POST'])
def set_directory():
    try:
        data = request.json
        directory = data.get('directory')
        if not directory:
            return jsonify({'success': False, 'error': 'Directory path required'})
        
        monitor.set_directory(directory)
        return jsonify({'success': True, 'message': f'Directory set to: {directory}'})
    except Exception as e:
        logger.error(f"Error setting directory: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/create-baseline', methods=['POST'])
def create_baseline():
    try:
        if not monitor.directory:
            return jsonify({'success': False, 'error': 'Please set a directory first'})
        
        success = monitor.create_baseline()
        if success:
            return jsonify({
                'success': True, 
                'message': f'Baseline created for {len(monitor.baseline)} files'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to create baseline'})
    except Exception as e:
        logger.error(f"Error creating baseline: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/scan', methods=['POST'])
def scan():
    try:
        if not monitor.baseline:
            if not monitor.load_baseline():
                return jsonify({'success': False, 'error': 'No baseline found. Create baseline first.'})
        
        success = monitor.scan_files()
        return jsonify({
            'success': success,
            'stats': monitor.stats,
            'alerts_count': len(monitor.alerts)
        })
    except Exception as e:
        logger.error(f"Error scanning files: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/start-monitoring', methods=['POST'])
def start_monitoring():
    try:
        data = request.json
        interval = data.get('interval', 2)
        
        if interval < 1 or interval > 60:
            return jsonify({'success': False, 'error': 'Interval must be between 1 and 60 seconds'})
        
        monitor.scan_interval = interval
        
        success = monitor.start_monitoring()
        return jsonify({
            'success': success,
            'message': f'Monitoring started with {interval}s interval',
            'is_monitoring': monitor.is_monitoring
        })
    except Exception as e:
        logger.error(f"Error starting monitoring: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/stop-monitoring', methods=['POST'])
def stop_monitoring():
    try:
        success = monitor.stop_monitoring()
        return jsonify({
            'success': success,
            'message': 'Monitoring stopped',
            'is_monitoring': monitor.is_monitoring
        })
    except Exception as e:
        logger.error(f"Error stopping monitoring: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/data')
def get_data():
    return jsonify({
        'stats': monitor.stats,
        'files': monitor.files_list,
        'alerts': monitor.alerts,
        'is_monitoring': monitor.is_monitoring,
        'directory': str(monitor.directory) if monitor.directory else None,
        'baseline_count': len(monitor.baseline)
    })

# NEW LOGGING ENDPOINTS
@app.route('/api/logs')
def get_logs():
    """Get operation logs with optional filtering"""
    try:
        operation_filter = request.args.get('operation')
        limit = int(request.args.get('limit', 100))
        
        logs = monitor.get_logs(operation_filter, limit)
        
        # Categorize logs by operation
        operations = {}
        for log in logs:
            op = log['operation']
            if op not in operations:
                operations[op] = []
            operations[op].append(log)
        
        return jsonify({
            'success': True,
            'logs': logs,
            'operations': list(operations.keys()),
            'total_logs': len(monitor.operation_logs),
            'filtered_count': len(logs)
        })
    except Exception as e:
        logger.error(f"Error getting logs: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/scan-history')
def get_scan_history():
    """Get scan performance history"""
    try:
        limit = int(request.args.get('limit', 10))
        history = monitor.get_scan_history(limit)
        
        # Calculate statistics
        total_scans = len(monitor.scan_history)
        avg_duration = 0
        if history:
            avg_duration = sum(scan['duration'] for scan in history) / len(history)
        
        return jsonify({
            'success': True,
            'history': history,
            'stats': {
                'total_scans': total_scans,
                'avg_duration': f'{avg_duration:.3f}s',
                'monitoring_active': monitor.is_monitoring
            }
        })
    except Exception as e:
        logger.error(f"Error getting scan history: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/logs/<operation>')
def get_logs_by_operation(operation):
    """Get logs for specific operation"""
    try:
        limit = int(request.args.get('limit', 50))
        logs = monitor.get_logs(operation, limit)
        
        # Count by status
        status_counts = {}
        for log in logs:
            status = log['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return jsonify({
            'success': True,
            'logs': logs,
            'operation': operation,
            'count': len(logs),
            'status_counts': status_counts
        })
    except Exception as e:
        logger.error(f"Error getting logs for operation {operation}: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/clear-logs', methods=['POST'])
def clear_logs():
    """Clear all logs"""
    try:
        success = monitor.clear_logs()
        return jsonify({
            'success': success,
            'message': 'All logs cleared'
        })
    except Exception as e:
        logger.error(f"Error clearing logs: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/status')
def get_status():
    """Get detailed system status"""
    return jsonify({
        'is_monitoring': monitor.is_monitoring,
        'directory': str(monitor.directory) if monitor.directory else None,
        'baseline_count': len(monitor.baseline),
        'scan_interval': monitor.scan_interval,
        'total_alerts': len(monitor.alerts),
        'total_logs': len(monitor.operation_logs),
        'total_scans': len(monitor.scan_history),
        'last_scan_stats': monitor.stats
    })

if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   🛡️  ANTI-RANSOMWARE FILE INTEGRITY MONITOR  🛡️         ║
    ║                                                           ║
    ║            Enhanced with Logging System                   ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    
    Features:
    - Real-time file monitoring
    - Detailed operation logging
    - Scan performance tracking
    - Web dashboard with log viewer
    
    Server starting...
    Open your browser and go to: http://localhost:5000
    
    Press Ctrl+C to stop the server
    """)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
# Global monitor instance
monitor = FileIntegrityMonitor()

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/set-directory', methods=['POST'])
def set_directory():
    try:
        data = request.json
        directory = data.get('directory')
        monitor.set_directory(directory)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/create-baseline', methods=['POST'])
def create_baseline():
    try:
        if not monitor.directory:
            return jsonify({'success': False, 'error': 'Please set a directory first'})
        monitor.create_baseline()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/scan', methods=['POST'])
def scan():
    try:
        if not monitor.baseline:
            monitor.load_baseline()
        monitor.scan_files()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/start-monitoring', methods=['POST'])
def start_monitoring():
    try:
        data = request.json
        interval = data.get('interval', 5)
        monitor.scan_interval = interval
        
        if not monitor.baseline:
            monitor.load_baseline()
        
        monitor.start_monitoring()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/stop-monitoring', methods=['POST'])
def stop_monitoring():
    try:
        monitor.stop_monitoring()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/data')
def get_data():
    return jsonify({
        'stats': monitor.stats,
        'files': monitor.files_list,
        'alerts': monitor.alerts,
        'is_monitoring': monitor.is_monitoring
    })

if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   🛡️  ANTI-RANSOMWARE FILE INTEGRITY MONITOR  🛡️         ║
    ║                                                           ║
    ║              Web Dashboard Version                        ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    
    Server starting...
    Open your browser and go to: http://localhost:5000
    
    Press Ctrl+C to stop the server
    """)
    
    app.run(debug=True, host='0.0.0.0', port=5000)