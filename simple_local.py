from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import threading
import time
import os
from base import Udemy, Scraper, LoginException, scraper_dict
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'local-development-key'

# Global variables to store application state
udemy_instance = None
scraper_instance = None
enrollment_thread = None
scraping_thread = None

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>DUCE - Local Test</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <div class="container mt-5">
            <h1 class="text-center mb-4">🎓 Discounted Udemy Course Enroller</h1>
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header bg-primary text-white">
                            <h5>Login to Udemy</h5>
                        </div>
                        <div class="card-body">
                            <form id="loginForm">
                                <div class="mb-3">
                                    <label class="form-label">Email</label>
                                    <input type="email" class="form-control" id="email" required>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">Password</label>
                                    <input type="password" class="form-control" id="password" required>
                                </div>
                                <button type="submit" class="btn btn-primary w-100">Login</button>
                            </form>
                            <div id="message" class="mt-3"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            document.getElementById('loginForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                
                try {
                    const response = await fetch('/login', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({email, password})
                    });
                    
                    const data = await response.json();
                    const messageDiv = document.getElementById('message');
                    
                    if (data.success) {
                        messageDiv.innerHTML = '<div class="alert alert-success">' + data.message + '</div>';
                        setTimeout(() => {
                            window.location.href = '/dashboard';
                        }, 1000);
                    } else {
                        messageDiv.innerHTML = '<div class="alert alert-danger">' + data.message + '</div>';
                    }
                } catch (error) {
                    document.getElementById('message').innerHTML = '<div class="alert alert-danger">Login failed: ' + error.message + '</div>';
                }
            });
        </script>
        
        <!-- Footer -->
        <footer class="bg-dark text-white text-center py-3 mt-5">
            <div class="container">
                <p class="mb-0">Made with ❤️ by <a href="https://t.me/meher_mankar" target="_blank" class="text-decoration-none text-info">Meher Mankar</a></p>
            </div>
        </footer>
    </body>
    </html>
    '''

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>DUCE Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-dark bg-dark">
            <div class="container">
                <span class="navbar-brand">DUCE Dashboard</span>
                <span class="navbar-text">Welcome, ''' + session.get('user_name', 'User') + '''</span>
            </div>
        </nav>
        
        <div class="container mt-4">
            <div class="row">
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header">Site Selection</div>
                        <div class="card-body">
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="Real Discount" id="rd" checked>
                                <label class="form-check-label" for="rd">Real Discount</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="Courson" id="courson" checked>
                                <label class="form-check-label" for="courson">Courson</label>
                            </div>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" value="Discudemy" id="du" checked>
                                <label class="form-check-label" for="du">Discudemy</label>
                            </div>
                            <button id="scrapeBtn" class="btn btn-info w-100 mt-3">Start Scraping</button>
                        </div>
                    </div>
                </div>
                
                <div class="col-md-8">
                    <div class="card">
                        <div class="card-header">Status</div>
                        <div class="card-body">
                            <div id="status" class="alert alert-info">Ready to start scraping...</div>
                            <button id="enrollBtn" class="btn btn-success w-100" style="display:none;">Start Enrollment</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            document.getElementById('scrapeBtn').addEventListener('click', async () => {
                const sites = Array.from(document.querySelectorAll('input:checked')).map(cb => cb.value);
                document.getElementById('status').innerHTML = '<div class="alert alert-info">Scraping started...</div>';
                
                try {
                    const response = await fetch('/scrape', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({sites})
                    });
                    
                    const data = await response.json();
                    if (data.success) {
                        document.getElementById('status').innerHTML = '<div class="alert alert-success">' + data.message + '</div>';
                        document.getElementById('enrollBtn').style.display = 'block';
                    } else {
                        document.getElementById('status').innerHTML = '<div class="alert alert-danger">' + data.message + '</div>';
                    }
                } catch (error) {
                    document.getElementById('status').innerHTML = '<div class="alert alert-danger">Error: ' + error.message + '</div>';
                }
            });
            
            document.getElementById('enrollBtn').addEventListener('click', async () => {
                document.getElementById('status').innerHTML = '<div class="alert alert-info">Enrollment started...</div>';
                
                try {
                    const response = await fetch('/enroll', {method: 'POST'});
                    const data = await response.json();
                    
                    if (data.success) {
                        document.getElementById('status').innerHTML = '<div class="alert alert-success">' + data.message + '</div>';
                    } else {
                        document.getElementById('status').innerHTML = '<div class="alert alert-danger">' + data.message + '</div>';
                    }
                } catch (error) {
                    document.getElementById('status').innerHTML = '<div class="alert alert-danger">Error: ' + error.message + '</div>';
                }
            });
        </script>
        
        <!-- Footer -->
        <footer class="bg-dark text-white text-center py-3 mt-5">
            <div class="container">
                <p class="mb-0">Made with ❤️ by <a href="https://t.me/meher_mankar" target="_blank" class="text-decoration-none text-info">Meher Mankar</a></p>
            </div>
        </footer>
    </body>
    </html>
    '''

@app.route('/login', methods=['POST'])
def login():
    global udemy_instance
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password are required'})
        
        udemy_instance = Udemy("web", debug=False)
        udemy_instance.load_settings()
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
        selected_sites = data.get('sites', ['Real Discount', 'Courson'])
        
        scraper_instance = Scraper(selected_sites)
        
        def scraping_worker():
            try:
                scraped_data = scraper_instance.get_scraped_courses(scrape_site_worker)
                udemy_instance.scraped_data = scraped_data
                print(f"Scraping completed! Found {len(scraped_data)} courses")
            except Exception as e:
                print(f"Scraping error: {e}")
        
        scraping_thread = threading.Thread(target=scraping_worker, daemon=True)
        scraping_thread.start()
        
        return jsonify({'success': True, 'message': 'Scraping started - check console for progress'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

def scrape_site_worker(site):
    """Worker function for scraping individual sites"""
    try:
        code_name = scraper_dict[site]
        print(f"Scraping {site}...")
        method = getattr(scraper_instance, code_name)
        method()
        print(f"{site} completed!")
    except Exception as e:
        print(f"Error scraping {site}: {e}")

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
                print(f"Starting enrollment for {len(udemy_instance.scraped_data)} courses...")
                udemy_instance.start_new_enroll()
                print(f"Enrollment completed!")
                print(f"Successfully enrolled: {udemy_instance.successfully_enrolled_c}")
                print(f"Already enrolled: {udemy_instance.already_enrolled_c}")
                print(f"Expired: {udemy_instance.expired_c}")
                print(f"Excluded: {udemy_instance.excluded_c}")
            except Exception as e:
                print(f"Enrollment error: {e}")
        
        enrollment_thread = threading.Thread(target=enrollment_worker, daemon=True)
        enrollment_thread.start()
        
        return jsonify({'success': True, 'message': 'Enrollment started - check console for progress'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    print("Starting DUCE Local Test Server...")
    print("Open your browser and go to: http://localhost:5000")
    print("Login with your Udemy credentials to test!")
    print("Check this console for scraping/enrollment progress")
    app.run(debug=True, host='0.0.0.0', port=5000)