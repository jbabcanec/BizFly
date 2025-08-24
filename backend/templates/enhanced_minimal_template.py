"""
Enhanced Minimal Template with Real Images
"""
from typing import Dict, Any
from .base_template import BaseTemplate
from services.image_service import BusinessImageSet


class EnhancedMinimalTemplate(BaseTemplate):
    def __init__(self):
        super().__init__("Enhanced Minimal", "universal")
        
    def get_structure(self) -> Dict[str, Any]:
        return {
            "sections": [
                "hero",
                "about", 
                "gallery",
                "services",
                "contact",
                "footer"
            ],
            "layout": "single-page",
            "navigation": "fixed-top"
        }
    
    def get_styles(self) -> Dict[str, Any]:
        return {
            "colors": {
                "primary": "#667eea",
                "secondary": "#764ba2", 
                "accent": "#FFD700",
                "background": "#ffffff",
                "text": "#333333"
            },
            "typography": {
                "heading_font": "Inter",
                "body_font": "Inter"
            }
        }
        
    def render(self, business_data: Dict[str, Any]) -> str:
        business = business_data.get("business", {})
        name = business.get("name", "Business Name")
        address = business.get("address", "")
        phone = business.get("phone", "")
        description = business_data.get("description", "")
        services = business_data.get("services", [])
        hours = business_data.get("hours", {})
        
        # Get real images
        business_type = business.get("business_type", "business")
        image_set = BusinessImageSet(business_type, name)
        images = image_set.to_template_data()
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Professional Services</title>
    <meta name="description" content="{description or f'{name} - Quality services in your area'}">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        
        .navbar {{
            position: fixed;
            top: 0;
            width: 100%;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 1000;
            padding: 1rem 0;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .nav-content {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .nav-brand {{
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 1.5rem;
            font-weight: 700;
            color: #1a1a1a;
        }}
        
        .nav-logo {{
            width: 40px;
            height: 40px;
            border-radius: 8px;
        }}
        
        .nav-menu {{
            display: flex;
            list-style: none;
            gap: 2rem;
        }}
        
        .nav-menu a {{
            color: #666;
            text-decoration: none;
            transition: color 0.3s;
        }}
        
        .nav-menu a:hover {{
            color: #667eea;
        }}
        
        .hero {{
            margin-top: 70px;
            height: 80vh;
            background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('{images["hero_image"]}') center/cover;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: white;
        }}
        
        .hero h1 {{
            font-size: 3.5rem;
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        
        .hero-subtitle {{
            font-size: 1.25rem;
            margin-bottom: 2rem;
            max-width: 600px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }}
        
        .btn {{
            display: inline-block;
            padding: 12px 30px;
            margin: 0 10px;
            border-radius: 50px;
            text-decoration: none;
            transition: all 0.3s;
            font-weight: 600;
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }}
        
        .btn-secondary {{
            background: white;
            color: #667eea;
        }}
        
        .btn-secondary:hover {{
            background: #f7f8fa;
        }}
        
        .section {{
            padding: 80px 0;
        }}
        
        .section h2 {{
            font-size: 2.5rem;
            margin-bottom: 2rem;
            text-align: center;
            color: #1a1a1a;
        }}
        
        .gallery {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 3rem;
        }}
        
        .gallery-item {{
            position: relative;
            overflow: hidden;
            border-radius: 12px;
            height: 250px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}
        
        .gallery-item:hover {{
            transform: scale(1.05);
        }}
        
        .gallery-item img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
        }}
        
        .services-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 30px;
            margin-top: 3rem;
        }}
        
        .service-card {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            transition: all 0.3s;
        }}
        
        .service-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        
        .contact {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .contact h2 {{
            color: white;
        }}
        
        .contact-info {{
            display: flex;
            justify-content: center;
            gap: 40px;
            flex-wrap: wrap;
            margin-top: 2rem;
        }}
        
        .contact-item {{
            text-align: center;
        }}
        
        .contact-item h3 {{
            margin-bottom: 10px;
            font-size: 1.2rem;
        }}
        
        .hours-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 2rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }}
        
        .hours-item {{
            display: flex;
            justify-content: space-between;
            padding: 10px;
            background: rgba(255,255,255,0.1);
            border-radius: 8px;
        }}
        
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 2rem;
            }}
            
            .nav-menu {{
                display: none;
            }}
            
            .gallery {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <div class="nav-content">
                <div class="nav-brand">
                    <img src="{images['logo']}" alt="{name} Logo" class="nav-logo">
                    {name}
                </div>
                <ul class="nav-menu">
                    <li><a href="#home">Home</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#gallery">Gallery</a></li>
                    <li><a href="#services">Services</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <section id="home" class="hero">
        <div class="container">
            <h1>{name}</h1>
            <p class="hero-subtitle">{description or 'Quality Services You Can Trust'}</p>
            <div class="hero-actions">
                <a href="#contact" class="btn btn-primary">Get in Touch</a>
                {f'<a href="tel:{phone}" class="btn btn-secondary">Call Now</a>' if phone else ''}
            </div>
        </div>
    </section>

    <section id="about" class="section">
        <div class="container">
            <h2>About Us</h2>
            <p style="text-align: center; max-width: 800px; margin: 0 auto; font-size: 1.1rem; color: #666;">
                {description or f'Welcome to {name}. We are dedicated to providing exceptional service to our community.'}
            </p>
        </div>
    </section>

    <section id="gallery" class="section" style="background: #f8f9fa;">
        <div class="container">
            <h2>Gallery</h2>
            <div class="gallery">
                {self._render_gallery(images['gallery'])}
            </div>
        </div>
    </section>

    {self._render_services_section(services)}

    <section id="contact" class="section contact">
        <div class="container">
            <h2>Contact Us</h2>
            <div class="contact-info">
                {f'''<div class="contact-item">
                    <h3>📍 Address</h3>
                    <p>{address}</p>
                </div>''' if address else ''}
                
                {f'''<div class="contact-item">
                    <h3>📞 Phone</h3>
                    <p><a href="tel:{phone}" style="color: white;">{phone}</a></p>
                </div>''' if phone else ''}
            </div>
            
            {self._render_hours(hours) if hours else ''}
        </div>
    </section>

    <footer style="background: #1a1a1a; color: white; padding: 20px 0; text-align: center;">
        <div class="container">
            <p>&copy; 2024 {name}. All rights reserved. | Powered by BizFly</p>
        </div>
    </footer>
</body>
</html>"""
        
        return html
    
    def _render_gallery(self, gallery_images: list) -> str:
        """Render gallery images"""
        if not gallery_images:
            return ""
        
        gallery_html = ""
        for idx, img_url in enumerate(gallery_images[:4]):  # Max 4 images
            gallery_html += f'''
                <div class="gallery-item">
                    <img src="{img_url}" alt="Gallery image {idx + 1}" loading="lazy">
                </div>
            '''
        
        return gallery_html
    
    def _render_services_section(self, services: list) -> str:
        """Render services section"""
        if not services:
            return ""
        
        services_html = '<section id="services" class="section"><div class="container">'
        services_html += '<h2>Our Services</h2><div class="services-grid">'
        
        for service in services[:6]:  # Max 6 services
            services_html += f'''
                <div class="service-card">
                    <h3 style="margin-bottom: 10px; color: #667eea;">✨ {service}</h3>
                    <p style="color: #666;">Professional {service.lower()} services with attention to detail and customer satisfaction.</p>
                </div>
            '''
        
        services_html += '</div></div></section>'
        return services_html
    
    def _render_hours(self, hours: dict) -> str:
        """Render business hours"""
        if not hours:
            return ""
        
        hours_html = '<div style="margin-top: 3rem;"><h3 style="margin-bottom: 1rem;">Business Hours</h3>'
        hours_html += '<div class="hours-grid">'
        
        for day, time in hours.items():
            hours_html += f'''
                <div class="hours-item">
                    <strong>{day.capitalize()}</strong>
                    <span>{time}</span>
                </div>
            '''
        
        hours_html += '</div></div>'
        return hours_html