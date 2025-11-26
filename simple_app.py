from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import threading
import time
import os
from base import Udemy, Scraper, LoginException, scraper_dict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Global variables
udemy_instance = None
scraper_instance = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    global udemy_instance
    try:
        data = request.get_json()
        login_method = data.get('method', 'password')
        
        udemy_instance = Udemy("web", debug=False)
        udemy_instance.load_settings()
        
        if login_method == 'cookies':
            client_id = data.get('client_id')
            access_token = data.get('access_token')
            csrf_token = data.get('csrf_token')
            
            if not all([client_id, access_token, csrf_token]):
                return jsonify({'success': False, 'message': 'All cookie values required'})
            
            udemy_instance.make_cookies(client_id, access_token, csrf_token)
            udemy_instance.get_session_info()
        else:
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return jsonify({'success': False, 'message': 'Email and password required'})
            
            udemy_instance.manual_login(email, password)
            udemy_instance.get_session_info()
        
        session['logged_in'] = True
        session['user_name'] = udemy_instance.display_name
        
        return jsonify({
            'success': True, 
            'message': f'Successfully logged in as {udemy_instance.display_name}',
            'user_name': udemy_instance.display_name
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/scrape', methods=['POST'])
def start_scraping():
    global scraper_instance
    
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Please login first'})
    
    try:
        data = request.get_json()
        selected_sites = data.get('sites', list(scraper_dict.keys()))
        
        scraper_instance = Scraper(selected_sites)
        scraped_data = scraper_instance.get_scraped_courses(lambda site: None)
        udemy_instance.scraped_data = scraped_data[:100]
        
        return jsonify({
            'success': True, 
            'message': f'Found {len(udemy_instance.scraped_data)} courses'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)