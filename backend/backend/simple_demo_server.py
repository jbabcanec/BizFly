#!/usr/bin/env python3
"""
BizFly Simple Demo Server
Runs without external dependencies to demonstrate core functionality
"""

import sys
sys.path.insert(0, '.')

import json
import tempfile
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from templates.template_manager import TemplateManager
from templates.minimal_template import MinimalTemplate
from templates.modern_template import ModernTemplate

class BizFlyDemoHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.serve_demo_page()
        elif parsed_path.path == '/generate':
            self.generate_website()
        elif parsed_path.path.startswith('/preview/'):
            self.serve_preview()
        else:
            self.send_error(404)
    
    def serve_demo_page(self):
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>BizFly Demo - Live Website Generator</title>
            <style>
                body { font-family: -apple-system,BlinkMacSystemFont,sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }
                .header { text-align: center; margin-bottom: 40px; }
                .demo-box { border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin: 20px 0; }
                .button { background: #007bff; color: white; padding: 12px 24px; border: none; border-radius: 6px; cursor: pointer; text-decoration: none; display: inline-block; }
                .button:hover { background: #0056b3; }
                .preview { border: 1px solid #ccc; height: 400px; width: 100%; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🚀 BizFly - Live Demo</h1>
                <p>Professional Website Generation Platform</p>
            </div>
            
            <div class="demo-box">
                <h2>Sample Business: Columbia Family Bakery</h2>
                <p><strong>Address:</strong> 1205 Rosewood Dr, Columbia, SC 29201</p>
                <p><strong>Phone:</strong> (803) 256-4828</p>
                <p><strong>Services:</strong> Fresh Bread, Wedding Cakes, Pastries, Catering</p>
                
                <h3>Generate Professional Website:</h3>
                <a href="/generate?template=minimal" class="button">Generate Minimal Template</a>
                <a href="/generate?template=modern" class="button">Generate Modern Template</a>
            </div>
            
            <div class="demo-box">
                <h2>✅ BizFly Features Demonstrated:</h2>
                <ul>
                    <li>✅ Business data processing</li>
                    <li>✅ Professional template rendering</li>
                    <li>✅ Mobile-responsive design</li>
                    <li>✅ Real-time website generation</li>
                    <li>✅ Multiple template options</li>
                </ul>
            </div>
            
            <div class="demo-box">
                <h2>🎯 In Full Production:</h2>
                <ul>
                    <li>🔍 Google Places API integration for business search</li>
                    <li>🤖 Claude AI agent for automatic business research</li>
                    <li>🎨 Rich React.js frontend interface</li>
                    <li>💾 PostgreSQL database for data storage</li>
                    <li>🚀 One-command deployment with Docker</li>
                </ul>
            </div>
        </body>
        </html>
        '''
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def generate_website(self):
        query = parse_qs(urlparse(self.path).query)
        template_type = query.get('template', ['minimal'])[0]
        
        # Sample business data
        business_data = {
            'business': {
                'name': 'Columbia Family Bakery',
                'address': '1205 Rosewood Dr, Columbia, SC 29201',
                'phone': '(803) 256-4828'
            },
            'description': 'Family-owned bakery serving fresh bread, pastries, and custom cakes for over 20 years.',
            'services': ['Fresh Bread Daily', 'Custom Wedding Cakes', 'Pastries & Croissants', 'Catering Services'],
            'hours': {
                'Monday': '6:00 AM - 6:00 PM',
                'Tuesday': '6:00 AM - 6:00 PM',
                'Wednesday': '6:00 AM - 6:00 PM',
                'Thursday': '6:00 AM - 6:00 PM',
                'Friday': '6:00 AM - 7:00 PM',
                'Saturday': '7:00 AM - 5:00 PM',
                'Sunday': '8:00 AM - 3:00 PM'
            }
        }
        
        try:
            if template_type == 'minimal':
                template = MinimalTemplate()
            else:
                template = ModernTemplate()
            
            website_html = template.render(business_data)
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(website_html.encode())
            
        except Exception as e:
            self.send_error(500, f"Generation failed: {e}")

def run_demo_server():
    print("🚀 Starting BizFly Demo Server...")
    print("=" * 40)
    
    server_address = ('localhost', 8080)
    httpd = HTTPServer(server_address, BizFlyDemoHandler)
    
    print(f"✅ BizFly Demo Server running at:")
    print(f"   🌐 http://localhost:8080")
    print(f"   📱 Mobile-friendly interface")
    print(f"   🎨 Live website generation")
    print()
    print("🎯 Demo Features:")
    print("   • Real-time website generation")
    print("   • Professional template rendering") 
    print("   • Mobile-responsive design")
    print("   • Multiple template options")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 40)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        httpd.server_close()

if __name__ == "__main__":
    run_demo_server()
