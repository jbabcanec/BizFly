#!/usr/bin/env python3
"""
Generate Ray's Diner website using BizFly system
This script demonstrates the full pipeline from business data to generated website
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.image_service import BusinessImageSet
from services.website_storage import WebsiteStorage
from templates.enhanced_minimal_template import EnhancedMinimalTemplate
import json
from datetime import datetime

def create_rays_diner_data():
    """Create comprehensive business data for Ray's Diner"""
    return {
        "business": {
            "name": "Ray's Diner",
            "address": "2530 Augusta Rd, West Columbia, SC 29169",
            "phone": "(803) 791-9947",
            "business_type": "restaurant",
            "latitude": 33.9937,
            "longitude": -81.0687,
            "google_maps_url": "https://maps.google.com/?cid=1234567890"
        },
        "description": "A beloved local diner serving authentic Southern comfort food for over 35 years. Ray's Diner is a hidden gem known for their famous grits, loaded omelets, and homemade meat loaf, all made from scratch daily.",
        "services": [
            "Breakfast All Day",
            "Lunch Specials", 
            "Dine-In Service",
            "Takeout Orders",
            "Catering Available",
            "Daily Specials"
        ],
        "hours": {
            "Monday": "5:30 AM - 3:00 PM",
            "Tuesday": "5:30 AM - 3:00 PM", 
            "Wednesday": "5:30 AM - 3:00 PM",
            "Thursday": "5:30 AM - 3:00 PM",
            "Friday": "5:30 AM - 3:00 PM",
            "Saturday": "5:30 AM - 3:00 PM",
            "Sunday": "6:00 AM - 3:00 PM"
        },
        "specialties": [
            "Ray's Famous Grits",
            "Loaded Omelets", 
            "Ray's Meat Loaf",
            "Chunky Hash Browns",
            "Homemade Biscuits",
            "Country Ham"
        ],
        "reviews": [
            {
                "rating": 5,
                "text": "Best grits I've ever had! Dense, creamy, and full of flavor. Ray's is a true local treasure.",
                "author": "Mike S."
            },
            {
                "rating": 5, 
                "text": "Hidden gem! The meat loaf is incredible and the service is always friendly. Been coming here for 20 years.",
                "author": "Sarah L."
            },
            {
                "rating": 4,
                "text": "Great diner food at excellent prices. The loaded omelet could feed two people!",
                "author": "John D."
            }
        ],
        "history": "Established in 1988, Ray's Diner has been a cornerstone of the West Columbia community for over three decades. What started as Ray's dream to serve honest, made-from-scratch Southern food has grown into a beloved local institution where friends and families gather for hearty meals and warm hospitality.",
        "images": [
            "Cozy diner interior with red vinyl booths and warm lighting",
            "Sizzling country breakfast with famous grits and eggs",
            "Ray's signature meat loaf with mashed potatoes and gravy",
            "Loaded omelet overflowing with cheese, ham, and vegetables"
        ]
    }

def main():
    """Generate Ray's Diner website"""
    print("🍽️  Generating Ray's Diner Website...")
    print("=" * 50)
    
    # Create business data
    business_data = create_rays_diner_data()
    business_name = business_data["business"]["name"]
    business_id = "rays_diner_columbia_sc"
    
    print(f"📋 Business: {business_name}")
    print(f"🆔 ID: {business_id}")
    
    # Get images
    print("\n📸 Sourcing images...")
    image_set = BusinessImageSet("restaurant", business_name)
    images = image_set.to_template_data()
    
    print(f"   Hero image: {images['hero_image'][:80]}...")
    print(f"   Gallery images: {len(images['gallery'])} images")
    print(f"   Logo: {images['logo'][:50]}...")
    
    # Generate website using enhanced template
    print("\n🎨 Generating website with Enhanced Minimal template...")
    template = EnhancedMinimalTemplate()
    html_content = template.render(business_data)
    
    print(f"   Generated {len(html_content):,} characters of HTML")
    
    # Save website
    print("\n💾 Saving website files...")
    storage = WebsiteStorage()
    
    # Create custom CSS for Ray's Diner
    custom_css = """
    /* Ray's Diner Custom Styling */
    :root {
        --rays-primary: #8B4513;
        --rays-secondary: #A0522D;
        --rays-gold: #FFD700;
        --rays-cream: #f8f6f0;
    }
    
    .hero {
        background-size: cover !important;
        background-position: center !important;
    }
    
    .nav-brand {
        color: var(--rays-primary) !important;
        font-weight: 800 !important;
    }
    
    .btn-primary {
        background: linear-gradient(135deg, var(--rays-primary) 0%, var(--rays-secondary) 100%) !important;
    }
    
    .service-card:hover {
        border-left: 4px solid var(--rays-gold);
    }
    
    .contact {
        background: linear-gradient(135deg, var(--rays-primary) 0%, var(--rays-secondary) 100%) !important;
    }
    """
    
    # Generate simple JavaScript for interactions
    custom_js = """
    // Ray's Diner Website JavaScript
    document.addEventListener('DOMContentLoaded', function() {
        // Smooth scrolling for navigation links
        const links = document.querySelectorAll('a[href^="#"]');
        links.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });
        
        // Add current time status for hours
        const now = new Date();
        const hour = now.getHours();
        const day = now.getDay(); // 0 = Sunday, 1 = Monday, etc.
        
        // Ray's Diner hours: 5:30 AM - 3:00 PM (Mon-Sat), 6:00 AM - 3:00 PM (Sun)
        let isOpen = false;
        if (day === 0) { // Sunday
            isOpen = hour >= 6 && hour < 15;
        } else { // Monday-Saturday  
            isOpen = hour >= 5 && hour < 15;
        }
        
        // Add open/closed indicator
        const header = document.querySelector('.nav-brand');
        if (header && isOpen) {
            header.innerHTML += ' <span style="color: #10b981; font-size: 0.8em;">• OPEN</span>';
        } else if (header) {
            header.innerHTML += ' <span style="color: #ef4444; font-size: 0.8em;">• CLOSED</span>';
        }
        
        console.log("🍽️ Ray's Diner website loaded successfully!");
    });
    """
    
    urls = storage.save_website(
        business_id=business_id,
        html=html_content,
        css=custom_css,
        js=custom_js,
        images=images,
        metadata={
            "business_name": business_name,
            "template": "Enhanced Minimal",
            "generated_by": "BizFly Demo Script",
            "business_type": "restaurant",
            "location": "West Columbia, SC"
        }
    )
    
    print(f"   ✅ Website saved successfully!")
    print(f"   📁 Files stored in: generated_websites/{business_id}/")
    
    # Display access URLs
    print("\n🌐 Access URLs:")
    print(f"   Preview: http://localhost:8000{urls['preview_url']}")
    print(f"   Static: http://localhost:8000{urls['static_url']}")
    print(f"   Download: http://localhost:8000{urls['download_url']}")
    
    # Create summary report
    print("\n📊 Generation Summary:")
    print(f"   Business: {business_name}")
    print(f"   Template: Enhanced Minimal")
    print(f"   Images: {len(images['gallery']) + 1} sourced")
    print(f"   Services: {len(business_data['services'])} listed")
    print(f"   Reviews: {len(business_data['reviews'])} included")
    print(f"   Hours: 7 days configured")
    
    print("\n✨ Ray's Diner website generation complete!")
    print("🚀 Visit the preview URL to see your generated website")
    
    return business_id, urls

if __name__ == "__main__":
    main()