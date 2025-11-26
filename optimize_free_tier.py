#!/usr/bin/env python3
"""
Optimize the application for Render free tier
- Reduce memory usage
- Limit concurrent operations
- Add sleep prevention
"""

import re

def optimize_base_py():
    with open('base.py', 'r') as f:
        content = f.read()
    
    # Reduce all ThreadPoolExecutor max_workers to 2
    content = re.sub(r'max_workers=\d+', 'max_workers=2', content)
    
    # Limit scraping pages
    content = content.replace('for page in range(1, 11)', 'for page in range(1, 6)')
    content = content.replace('for page in range(1, 6)', 'for page in range(1, 4)')
    
    # Limit course processing
    content = content.replace('for item in all_items', 'for item in all_items[:30]')
    
    with open('base.py', 'w') as f:
        f.write(content)

def add_keepalive():
    with open('web_app.py', 'r') as f:
        content = f.read()
    
    # Add keepalive endpoint
    keepalive_code = '''
@app.route('/keepalive')
def keepalive():
    return jsonify({'status': 'alive', 'timestamp': time.time()})
'''
    
    # Insert before the main app section
    content = content.replace('if __name__ == \'__main__\':', keepalive_code + '\nif __name__ == \'__main__\':')
    
    with open('web_app.py', 'w') as f:
        f.write(content)

if __name__ == '__main__':
    optimize_base_py()
    add_keepalive()
    print("Optimization complete!")