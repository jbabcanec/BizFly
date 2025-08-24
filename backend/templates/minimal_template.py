from typing import Dict, Any
from .base_template import BaseTemplate


class MinimalTemplate(BaseTemplate):
    def __init__(self):
        super().__init__("Minimal", "universal")
        
    def get_structure(self) -> Dict[str, Any]:
        return {
            "sections": [
                "hero",
                "about",
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
                "primary": "#0f172a",
                "secondary": "#475569",
                "accent": "#0ea5e9",
                "background": "#ffffff",
                "text": "#334155",
                "light": "#f8fafc",
                "success": "#10b981",
                "gradient_start": "#667eea",
                "gradient_end": "#764ba2"
            },
            "typography": {
                "heading_font": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, system-ui, sans-serif",
                "body_font": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, system-ui, sans-serif",
                "base_size": "16px"
            },
            "spacing": {
                "section_padding": "100px",
                "container_max": "1280px"
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
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Professional Services</title>
    <meta name="description" content="{description or f'{name} - Quality services in your area'}">
    <style>
        {self._generate_css()}
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <div class="nav-brand">{name}</div>
            <ul class="nav-menu">
                <li><a href="#home">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#services">Services</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
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
            <p>{description or f'Welcome to {name}. We are dedicated to providing exceptional service to our community.'}</p>
        </div>
    </section>

    {self._render_services(services)}
    {self._render_contact(business)}
    
    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 {name}. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>"""
        return html
    
    def _generate_css(self) -> str:
        styles = self.get_styles()
        colors = styles["colors"]
        typography = styles["typography"]
        spacing = styles["spacing"]
        
        return f"""
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        :root {{
            --primary: {colors['primary']};
            --secondary: {colors['secondary']};
            --accent: {colors['accent']};
            --background: {colors['background']};
            --text: {colors['text']};
            --light: {colors['light']};
            --success: {colors['success']};
            --gradient-start: {colors['gradient_start']};
            --gradient-end: {colors['gradient_end']};
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        ::selection {{
            background: rgba(14, 165, 233, 0.2);
            color: var(--primary);
        }}
        
        html {{
            scroll-behavior: smooth;
        }}
        
        body {{
            font-family: {typography['body_font']};
            font-size: {typography['base_size']};
            line-height: 1.7;
            color: var(--text);
            background: var(--background);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}
        
        .container {{
            max-width: {spacing['container_max']};
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        .navbar {{
            position: fixed;
            top: 0;
            width: 100%;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(0, 0, 0, 0.05);
            z-index: 1000;
            padding: 1rem 0;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .navbar.scrolled {{
            background: rgba(255, 255, 255, 0.98);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }}
        
        .navbar .container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .nav-brand {{
            font-size: 1.25rem;
            font-weight: 600;
            color: {colors['primary']};
        }}
        
        .nav-menu {{
            display: flex;
            list-style: none;
            gap: 2rem;
        }}
        
        .nav-menu a {{
            color: {colors['secondary']};
            text-decoration: none;
            transition: color 0.3s;
        }}
        
        .nav-menu a:hover {{
            color: {colors['accent']};
        }}
        
        .hero {{
            padding: calc({spacing['section_padding']} + 80px) 0 {spacing['section_padding']} 0;
            text-align: center;
            background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
            color: white;
            position: relative;
            overflow: hidden;
        }}
        
        .hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="1" fill="white" opacity="0.1"/><circle cx="80" cy="80" r="1" fill="white" opacity="0.1"/><circle cx="60" cy="20" r="0.5" fill="white" opacity="0.1"/><circle cx="40" cy="80" r="0.5" fill="white" opacity="0.1"/></svg>') repeat;
            animation: float 20s linear infinite;
        }}
        
        @keyframes float {{
            0% {{ transform: translateY(0) translateX(0); }}
            33% {{ transform: translateY(-20px) translateX(10px); }}
            66% {{ transform: translateY(10px) translateX(-10px); }}
            100% {{ transform: translateY(0) translateX(0); }}
        }}
        
        .hero h1 {{
            font-size: 3rem;
            margin-bottom: 1rem;
            font-family: {typography['heading_font']};
        }}
        
        .hero-subtitle {{
            font-size: 1.25rem;
            margin-bottom: 2rem;
            opacity: 0.9;
        }}
        
        .hero-actions {{
            display: flex;
            gap: 1rem;
            justify-content: center;
        }}
        
        .btn {{
            padding: 1rem 2.5rem;
            border-radius: 2rem;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-weight: 600;
            font-size: 1.1rem;
            position: relative;
            overflow: hidden;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .btn::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 100%);
            transform: translateX(-100%);
            transition: transform 0.6s;
        }}
        
        .btn:hover::before {{
            transform: translateX(100%);
        }}
        
        .btn-primary {{
            background: white;
            color: var(--primary);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
        }}
        
        .btn-primary:hover {{
            transform: translateY(-3px);
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.18);
            background: #f8fafc;
        }}
        
        .btn-secondary {{
            background: transparent;
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.8);
        }}
        
        .btn-secondary:hover {{
            background: rgba(255, 255, 255, 0.15);
            border-color: white;
            transform: translateY(-2px);
        }}
        
        .section {{
            padding: {spacing['section_padding']} 0;
        }}
        
        .section h2 {{
            font-size: 2.5rem;
            margin-bottom: 2rem;
            text-align: center;
            font-family: {typography['heading_font']};
            color: {colors['primary']};
        }}
        
        .services-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }}
        
        .service-card {{
            padding: 2.5rem;
            background: white;
            border-radius: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 25px rgba(0, 0, 0, 0.08);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(0, 0, 0, 0.05);
        }}
        
        .service-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
            background: linear-gradient(90deg, var(--accent) 0%, var(--gradient-start) 100%);
        }}
        
        .service-card:hover {{
            transform: translateY(-8px);
            box-shadow: 0 16px 50px rgba(0, 0, 0, 0.15);
        }}
        
        .service-card h3 {{
            margin-bottom: 1rem;
            color: var(--primary);
            font-weight: 700;
            font-size: 1.25rem;
        }}
        
        .service-card p {{
            color: var(--secondary);
            line-height: 1.6;
        }}
        
        .contact-info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }}
        
        .contact-item {{
            text-align: center;
        }}
        
        .contact-item h3 {{
            color: {colors['accent']};
            margin-bottom: 1rem;
        }}
        
        .footer {{
            background: {colors['primary']};
            color: white;
            text-align: center;
            padding: 2rem 0;
            margin-top: 4rem;
        }}
        
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 2rem;
            }}
            
            .nav-menu {{
                gap: 1rem;
                font-size: 0.9rem;
            }}
            
            .hero-actions {{
                flex-direction: column;
                align-items: center;
            }}
        }}
        """
    
    def _render_services(self, services: list) -> str:
        if not services:
            return ""
        
        service_items = "".join([
            f"""<div class="service-card">
                <h3>{service}</h3>
                <p>Professional {service.lower()} services</p>
            </div>"""
            for service in services[:6]
        ])
        
        return f"""
        <section id="services" class="section">
            <div class="container">
                <h2>Our Services</h2>
                <div class="services-grid">
                    {service_items}
                </div>
            </div>
        </section>
        """
    
    def _render_contact(self, business: Dict[str, Any]) -> str:
        address = business.get("address", "")
        phone = business.get("phone", "")
        
        return f"""
        <section id="contact" class="section">
            <div class="container">
                <h2>Contact Us</h2>
                <div class="contact-info">
                    {f'''<div class="contact-item">
                        <h3>Address</h3>
                        <p>{address}</p>
                    </div>''' if address else ''}
                    {f'''<div class="contact-item">
                        <h3>Phone</h3>
                        <p><a href="tel:{phone}">{phone}</a></p>
                    </div>''' if phone else ''}
                </div>
            </div>
        </section>
        """