#!/bin/bash

echo "🚀 Deployment Helper Script"
echo "=========================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit for deployment"
fi

echo ""
echo "Choose deployment platform:"
echo "1) Render"
echo "2) Vercel"
echo "3) Test Locally"
echo ""
read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "📋 Render Deployment Steps:"
        echo "1. Push code to GitHub"
        echo "2. Go to https://render.com"
        echo "3. Click 'New +' → 'Web Service'"
        echo "4. Connect your GitHub repo"
        echo "5. Use these settings:"
        echo "   - Build: pip install -r requirements_web.txt"
        echo "   - Start: gunicorn --worker-class eventlet -w 1 wsgi:app"
        echo ""
        read -p "Push to GitHub now? (y/n): " push
        if [ "$push" = "y" ]; then
            read -p "Enter GitHub repo URL: " repo
            git remote add origin $repo
            git push -u origin main
            echo "✅ Pushed to GitHub!"
        fi
        ;;
    2)
        echo ""
        echo "📋 Installing Vercel CLI..."
        npm install -g vercel
        echo ""
        echo "🚀 Deploying to Vercel..."
        vercel
        ;;
    3)
        echo ""
        echo "🧪 Testing locally..."
        pip install -r requirements_web.txt
        python web_app.py
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "✅ Done!"