#!/usr/bin/env python3
"""
Optimize for fast scraping while maintaining memory efficiency
"""

import re

def optimize_for_speed():
    with open('base.py', 'r') as f:
        content = f.read()
    
    # Increase workers for speed but keep memory efficient
    content = re.sub(r'max_workers=2', 'max_workers=4', content)
    
    # Reduce timeout delays for faster processing
    content = content.replace('time.sleep(3.5)', 'time.sleep(1)')
    content = content.replace('time.sleep(0.2)', 'time.sleep(0.1)')
    
    # Reduce pages but increase workers for faster parallel processing
    content = content.replace('for page in range(1, 4)', 'for page in range(1, 3)')
    
    # Limit items but process faster
    content = content.replace('for item in all_items[:30]', 'for item in all_items[:20]')
    
    with open('base.py', 'w') as f:
        f.write(content)

if __name__ == '__main__':
    optimize_for_speed()
    print("Fast scraping optimization complete!")