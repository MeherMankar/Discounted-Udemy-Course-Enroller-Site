from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit
import threading
import time
import os
import gc
from base import Udemy, Scraper, LoginException, scraper_dict
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
socketio = SocketIO(app, cors_allowed_origins="*", logger=False, engineio_logger=False)

# Global variables to store application state
udemy_instance = None
scraper_instance = None
enrollment_thread = None
scraping_thread = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cookie-help')
def cookie_help():
    help_text = """
    <h2>How to Get Udemy Cookies</h2>
    <ol>
        <li>Login to Udemy in your browser</li>
        <li>Press F12 to open Developer Tools</li>
        <li>Go to Application/Storage tab</li>
        <li>Click on Cookies → https://www.udemy.com</li>
        <li>Copy these values:
            <ul>
                <li><strong>client_id</strong></li>
                <li><strong>access_token</strong></li>
                <li><strong>csrftoken</strong> (use as csrf_token)</li>
            </ul>
        </li>
        <li>Use Cookie Login method in the app</li>
    </ol>
    <p><strong>Note:</strong> Cookies expire after some time, you may need to refresh them.</p>
    """
    return help_text

@app.route('/login', methods=['POST'])
def login():
    global udemy_instance
    try:
        data = request.get_json()
        login_method = data.get('method', 'password')
        
        udemy_instance = Udemy("web", debug=False)
        udemy_instance.load_settings()
        
        if login_method == 'cookies':
            # Cookie-based login
            client_id = data.get('client_id')
            access_token = data.get('access_token')
            csrf_token = data.get('csrf_token')
            
            if not all([client_id, access_token, csrf_token]):
                return jsonify({'success': False, 'message': 'All cookie values (client_id, access_token, csrf_token) are required'})
            
            udemy_instance.make_cookies(client_id, access_token, csrf_token)
            udemy_instance.get_session_info()
        else:
            # Email/password login
            email = data.get('email')
            password = data.get('password')
            
            if not email or not password:
                return jsonify({'success': False, 'message': 'Email and password are required'})
            
            udemy_instance.manual_login(email, password)
            udemy_instance.get_session_info()
        
        session['logged_in'] = True
        session['user_name'] = udemy_instance.display_name
        
        return jsonify({
            'success': True, 
            'message': f'Successfully logged in as {udemy_instance.display_name}',
            'user_name': udemy_instance.display_name
        })
        
    except LoginException as e:
        return jsonify({'success': False, 'message': str(e)})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Login failed: {str(e)}'})

@app.route('/scrape', methods=['POST'])
def start_scraping():
    global scraper_instance, scraping_thread
    
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Please login first'})
    
    try:
        data = request.get_json()
        selected_sites = data.get('sites', list(scraper_dict.keys()))
        
        scraper_instance = Scraper(selected_sites)
        
        def scraping_worker():
            try:
                scraped_data = scraper_instance.get_scraped_courses(scrape_site_worker)
                udemy_instance.scraped_data = scraped_data
                socketio.emit('scraping_complete', {
                    'total_courses': len(scraped_data),
                    'message': f'Found {len(scraped_data)} courses'
                })
            except Exception as e:
                socketio.emit('scraping_error', {'message': str(e)})
            finally:
                # Clean up memory
                gc.collect()
        
        scraping_thread = threading.Thread(target=scraping_worker, daemon=True)
        scraping_thread.start()
        
        return jsonify({'success': True, 'message': 'Scraping started'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

def scrape_site_worker(site):
    """Worker function for scraping individual sites"""
    try:
        code_name = scraper_dict[site]
        method = getattr(scraper_instance, code_name)
        method()
        
        # Emit progress updates
        socketio.emit('scraping_progress', {
            'site': site,
            'progress': getattr(scraper_instance, f"{code_name}_progress"),
            'total': getattr(scraper_instance, f"{code_name}_length"),
            'completed': getattr(scraper_instance, f"{code_name}_done")
        })
        
    except Exception as e:
        socketio.emit('scraping_error', {'site': site, 'error': str(e)})

@app.route('/enroll', methods=['POST'])
def start_enrollment():
    global enrollment_thread
    
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Please login first'})
    
    if not hasattr(udemy_instance, 'scraped_data'):
        return jsonify({'success': False, 'message': 'Please scrape courses first'})
    
    try:
        def enrollment_worker():
            try:
                # Set up progress callback
                def update_progress():
                    socketio.emit('enrollment_progress', {
                        'current_course': udemy_instance.total_courses_processed,
                        'total_courses': udemy_instance.total_courses,
                        'successfully_enrolled': udemy_instance.successfully_enrolled_c,
                        'already_enrolled': udemy_instance.already_enrolled_c,
                        'expired': udemy_instance.expired_c,
                        'excluded': udemy_instance.excluded_c,
                        'amount_saved': float(udemy_instance.amount_saved_c),
                        'currency': udemy_instance.currency,
                        'current_course_title': udemy_instance.course.title if hasattr(udemy_instance, 'course') and udemy_instance.course else 'N/A'
                    })
                
                udemy_instance.update_progress = update_progress
                udemy_instance.start_new_enroll()
                
                socketio.emit('enrollment_complete', {
                    'successfully_enrolled': udemy_instance.successfully_enrolled_c,
                    'already_enrolled': udemy_instance.already_enrolled_c,
                    'expired': udemy_instance.expired_c,
                    'excluded': udemy_instance.excluded_c,
                    'amount_saved': float(udemy_instance.amount_saved_c),
                    'currency': udemy_instance.currency
                })
                
            except Exception as e:
                socketio.emit('enrollment_error', {'message': str(e)})
            finally:
                # Clean up memory
                gc.collect()
        
        enrollment_thread = threading.Thread(target=enrollment_worker, daemon=True)
        enrollment_thread.start()
        
        return jsonify({'success': True, 'message': 'Enrollment started'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Please login first'})
    
    if request.method == 'GET':
        return jsonify({
            'success': True,
            'settings': udemy_instance.settings
        })
    
    try:
        data = request.get_json()
        udemy_instance.settings.update(data)
        udemy_instance.save_settings()
        return jsonify({'success': True, 'message': 'Settings saved'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/status')
def status():
    return jsonify({
        'logged_in': session.get('logged_in', False),
        'user_name': session.get('user_name', ''),
        'scraping_active': scraping_thread and scraping_thread.is_alive() if scraping_thread else False,
        'enrollment_active': enrollment_thread and enrollment_thread.is_alive() if enrollment_thread else False
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, debug=False, host='0.0.0.0', port=port)