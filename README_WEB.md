# Discounted Udemy Course Enroller - Web Interface

A web-based version of the popular Discounted Udemy Course Enroller with full functionality accessible through your browser.

## Features

- **Web-based Interface**: Modern, responsive design accessible from any browser
- **Real-time Updates**: Live progress tracking using WebSocket connections
- **Full Functionality**: All features from the original desktop application
- **Email/Password Login**: Secure login using your Udemy credentials
- **Multi-site Scraping**: Support for all major coupon sites
- **Live Statistics**: Real-time enrollment statistics and progress
- **Course Filtering**: Advanced filtering options (same as desktop version)

## Quick Start

### Method 1: One-Click Launch
```bash
python run_web.py
```
This will automatically:
- Install required dependencies
- Start the web server
- Open your browser to http://localhost:5000

### Method 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements_web.txt

# Start the web application
python web_app.py
```

Then open your browser and go to: http://localhost:5000

## Usage

1. **Login**: Enter your Udemy email and password
2. **Select Sites**: Choose which coupon sites to scrape from
3. **Start Scraping**: Click "Start Scraping" to find courses
4. **Start Enrollment**: Once scraping is complete, click "Start Enrollment"
5. **Monitor Progress**: Watch real-time statistics and progress updates

## Features Overview

### Login System
- Secure email/password authentication
- Session management
- Automatic cookie handling

### Course Scraping
- **Real Discount**: Premium coupon aggregator
- **Courson**: Fast API-based scraping
- **IDownloadCoupons**: Comprehensive course database
- **E-next**: Job portal with course listings
- **Discudemy**: Popular free course site
- **Udemy Freebies**: Dedicated free course platform
- **Course Joiner**: Community-driven coupons
- **Course Vania**: Educational course aggregator

### Real-time Features
- Live progress bars for scraping and enrollment
- Real-time statistics updates
- WebSocket-based communication
- Responsive progress indicators

### Statistics Tracking
- Successfully enrolled courses
- Already enrolled courses
- Expired coupons
- Excluded courses (by filters)
- Total amount saved

## Configuration

The web application uses the same settings system as the desktop version:
- Settings are stored in `duce-web-settings.json`
- All filtering options available (categories, languages, ratings, etc.)
- Instructor and keyword exclusion lists
- Course update threshold settings

## Technical Details

### Architecture
- **Backend**: Flask with SocketIO for real-time communication
- **Frontend**: Bootstrap 5 with vanilla JavaScript
- **Threading**: Background workers for scraping and enrollment
- **Session Management**: Flask sessions for user state

### API Endpoints
- `POST /login` - User authentication
- `POST /scrape` - Start course scraping
- `POST /enroll` - Start course enrollment
- `GET /settings` - Get current settings
- `POST /settings` - Update settings
- `GET /status` - Get application status

### WebSocket Events
- `scraping_progress` - Scraping progress updates
- `scraping_complete` - Scraping completion
- `enrollment_progress` - Enrollment progress updates
- `enrollment_complete` - Enrollment completion
- `*_error` - Error notifications

## Security Notes

- Credentials are only stored in session (not persistent)
- All communication happens locally (localhost)
- Same security model as the original desktop application
- No data is sent to external servers except Udemy

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Change port in web_app.py or kill existing process
   netstat -ano | findstr :5000
   ```

2. **Dependencies Not Installing**
   ```bash
   # Upgrade pip first
   python -m pip install --upgrade pip
   pip install -r requirements_web.txt
   ```

3. **Browser Not Opening**
   - Manually navigate to http://localhost:5000
   - Check if firewall is blocking the connection

4. **Login Issues**
   - Ensure correct Udemy credentials
   - Check internet connection
   - Verify Udemy account is not locked

### Performance Tips

- Close unnecessary browser tabs for better performance
- Use Chrome/Firefox for best WebSocket support
- Ensure stable internet connection for scraping

## Development

### File Structure
```
├── web_app.py          # Main Flask application
├── templates/
│   └── index.html      # Main web interface
├── static/             # Static assets (CSS, JS, images)
├── requirements_web.txt # Web-specific dependencies
└── run_web.py          # Launch script
```

### Extending the Application

1. **Adding New Sites**: Extend the `scraper_dict` in `base.py`
2. **Custom Filters**: Modify settings structure
3. **UI Improvements**: Edit `templates/index.html`
4. **API Extensions**: Add new routes in `web_app.py`

## License

Same license as the original project. See LICENSE file.

## Support

- GitHub Issues: Report bugs and feature requests
- Discord: Join the community server
- Documentation: Check the main README.md

---

**Note**: This web interface provides the same functionality as the desktop GUI and CLI versions, but accessible through any modern web browser.