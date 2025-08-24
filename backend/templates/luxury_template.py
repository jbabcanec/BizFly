from typing import Dict, Any
from .base_template import BaseTemplate


class LuxuryTemplate(BaseTemplate):
    def __init__(self):
        super().__init__("Luxury Business", "premium")
        
    def get_structure(self) -> Dict[str, Any]:
        return {
            "sections": [
                "hero",
                "about",
                "services",
                "gallery",
                "testimonials",
                "contact",
                "footer"
            ],
            "layout": "single-page",
            "navigation": "glass-top"
        }
    
    def get_styles(self) -> Dict[str, Any]:
        return {
            "colors": {
                "primary": "#1a1a2e",
                "secondary": "#16213e",
                "accent": "#e94560",
                "gold": "#c9b037",
                "background": "#ffffff",
                "text": "#2d3748",
                "light": "#f7fafc",
                "dark": "#0f0f23"
            },
            "typography": {
                "heading_font": "'Playfair Display', Georgia, serif",
                "body_font": "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
                "base_size": "17px"
            },
            "spacing": {
                "section_padding": "120px",
                "container_max": "1400px"
            }
        }
    
    def render(self, business_data: Dict[str, Any]) -> str:
        business = business_data.get("business", {})
        name = business.get("name", "Business Name")
        address = business.get("address", "")
        phone = business.get("phone", "")
        description = business_data.get("description", "")
        services = business_data.get("services", [])
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Luxury Experience</title>
    <meta name="description" content="{description or f'{name} - Premium services with unmatched excellence'}">
    <style>
        {self._generate_css()}
    </style>
</head>
<body>
    <nav class="navbar" id="navbar">
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
        <div class="hero-background"></div>
        <div class="hero-overlay"></div>
        <div class="container">
            <div class="hero-content">
                <h1 class="hero-title">{name}</h1>
                <p class="hero-subtitle">{description or 'Luxury. Excellence. Uncompromising Quality.'}</p>
                <div class="hero-actions">
                    <a href="#contact" class="btn btn-primary">Experience Excellence</a>
                    {f'<a href="tel:{phone}" class="btn btn-secondary">Call Now</a>' if phone else ''}
                </div>
            </div>
        </div>
        <div class="scroll-indicator">
            <div class="scroll-arrow"></div>
        </div>
    </section>

    <section id="about" class="section about">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">About Our Excellence</h2>
                <div class="section-divider"></div>
            </div>
            <div class="about-content">
                <p class="about-text">{description or f'Welcome to {name}, where luxury meets exceptional service. We are dedicated to providing an unparalleled experience that exceeds your every expectation.'}</p>
            </div>
        </div>
    </section>

    {self._render_services(services)}
    {self._render_contact(business)}
    
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-brand">
                    <h3>{name}</h3>
                    <p>Excellence in every detail</p>
                </div>
                <div class="footer-info">
                    <p>&copy; 2024 {name}. All rights reserved.</p>
                </div>
            </div>
        </div>
    </footer>

    <script>
        // Smooth scrolling and navbar effects
        window.addEventListener('scroll', function() {{
            const navbar = document.getElementById('navbar');
            if (window.scrollY > 100) {{
                navbar.classList.add('scrolled');
            }} else {{
                navbar.classList.remove('scrolled');
            }}
        }});

        // Smooth scroll for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});
    </script>
</body>
</html>"""
        return html
    
    def _generate_css(self) -> str:
        styles = self.get_styles()
        colors = styles["colors"]
        typography = styles["typography"]
        spacing = styles["spacing"]
        
        return f"""
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
        
        :root {{
            --primary: {colors['primary']};
            --secondary: {colors['secondary']};
            --accent: {colors['accent']};
            --gold: {colors['gold']};
            --background: {colors['background']};
            --text: {colors['text']};
            --light: {colors['light']};
            --dark: {colors['dark']};
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        ::selection {{
            background: var(--gold);
            color: var(--dark);
        }}
        
        html {{
            scroll-behavior: smooth;
        }}
        
        body {{
            font-family: {typography['body_font']};
            font-size: {typography['base_size']};
            line-height: 1.8;
            color: var(--text);
            background: var(--background);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            overflow-x: hidden;
        }}
        
        .container {{
            max-width: {spacing['container_max']};
            margin: 0 auto;
            padding: 0 2rem;
        }}
        
        .navbar {{
            position: fixed;
            top: 0;
            width: 100%;
            background: rgba(26, 26, 46, 0.1);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            z-index: 1000;
            padding: 1.5rem 0;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .navbar.scrolled {{
            background: rgba(26, 26, 46, 0.95);
            backdrop-filter: blur(30px);
            box-shadow: 0 8px 40px rgba(0, 0, 0, 0.12);
            padding: 1rem 0;
        }}
        
        .navbar .container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .nav-brand {{
            font-family: {typography['heading_font']};
            font-size: 1.8rem;
            font-weight: 600;
            color: white;
            text-decoration: none;
        }}
        
        .nav-menu {{
            display: flex;
            list-style: none;
            gap: 2.5rem;
        }}
        
        .nav-menu a {{
            color: rgba(255, 255, 255, 0.9);
            text-decoration: none;
            font-weight: 500;
            position: relative;
            transition: all 0.3s;
        }}
        
        .nav-menu a::after {{
            content: '';
            position: absolute;
            bottom: -8px;
            left: 50%;
            width: 0;
            height: 2px;
            background: var(--gold);
            transition: all 0.3s;
            transform: translateX(-50%);
        }}
        
        .nav-menu a:hover {{
            color: white;
        }}
        
        .nav-menu a:hover::after {{
            width: 100%;
        }}
        
        .hero {{
            height: 100vh;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            overflow: hidden;
        }}
        
        .hero-background {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 50%, var(--accent) 100%);
            z-index: 1;
        }}
        
        .hero-background::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="20" cy="20" r="0.5" fill="white" opacity="0.03"/><circle cx="80" cy="80" r="0.3" fill="white" opacity="0.05"/><circle cx="40" cy="60" r="0.2" fill="white" opacity="0.04"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            animation: grain 20s linear infinite;
        }}
        
        @keyframes grain {{
            0%, 100% {{ transform: translate(0, 0); }}
            10% {{ transform: translate(-5%, -10%); }}
            20% {{ transform: translate(-15%, 5%); }}
            30% {{ transform: translate(7%, -25%); }}
            40% {{ transform: translate(-5%, 25%); }}
            50% {{ transform: translate(-15%, 10%); }}
            60% {{ transform: translate(15%, 0%); }}
            70% {{ transform: translate(0%, 15%); }}
            80% {{ transform: translate(3%, 35%); }}
            90% {{ transform: translate(-10%, 10%); }}
        }}
        
        .hero-overlay {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(ellipse at center, transparent 0%, rgba(0,0,0,0.1) 100%);
            z-index: 2;
        }}
        
        .hero-content {{
            position: relative;
            z-index: 3;
            max-width: 800px;
            margin: 0 auto;
            animation: fadeInUp 1.2s ease-out;
        }}
        
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(60px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .hero-title {{
            font-family: {typography['heading_font']};
            font-size: clamp(3rem, 8vw, 6rem);
            font-weight: 600;
            color: white;
            margin-bottom: 1.5rem;
            text-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }}
        
        .hero-subtitle {{
            font-size: 1.4rem;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 3rem;
            font-weight: 300;
            letter-spacing: 0.5px;
        }}
        
        .hero-actions {{
            display: flex;
            gap: 2rem;
            justify-content: center;
            flex-wrap: wrap;
        }}
        
        .btn {{
            padding: 1.2rem 3rem;
            border-radius: 0;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            font-weight: 600;
            font-size: 1rem;
            position: relative;
            overflow: hidden;
            text-transform: uppercase;
            letter-spacing: 1px;
            border: 2px solid transparent;
        }}
        
        .btn::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }}
        
        .btn:hover::before {{
            left: 100%;
        }}
        
        .btn-primary {{
            background: var(--gold);
            color: var(--dark);
            box-shadow: 0 8px 32px rgba(201, 176, 55, 0.3);
        }}
        
        .btn-primary:hover {{
            transform: translateY(-3px);
            box-shadow: 0 16px 40px rgba(201, 176, 55, 0.4);
            background: #d4c44a;
        }}
        
        .btn-secondary {{
            background: transparent;
            color: white;
            border-color: rgba(255, 255, 255, 0.6);
        }}
        
        .btn-secondary:hover {{
            background: rgba(255, 255, 255, 0.1);
            border-color: white;
            transform: translateY(-2px);
        }}
        
        .scroll-indicator {{
            position: absolute;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            z-index: 3;
        }}
        
        .scroll-arrow {{
            width: 2px;
            height: 60px;
            background: rgba(255, 255, 255, 0.6);
            position: relative;
            animation: scroll 2s infinite;
        }}
        
        .scroll-arrow::after {{
            content: '';
            position: absolute;
            bottom: -8px;
            left: 50%;
            transform: translateX(-50%);
            width: 0;
            height: 0;
            border-left: 6px solid transparent;
            border-right: 6px solid transparent;
            border-top: 8px solid rgba(255, 255, 255, 0.6);
        }}
        
        @keyframes scroll {{
            0%, 100% {{ opacity: 0.6; }}
            50% {{ opacity: 1; }}
        }}
        
        .section {{
            padding: {spacing['section_padding']} 0;
            position: relative;
        }}
        
        .section-header {{
            text-align: center;
            margin-bottom: 5rem;
        }}
        
        .section-title {{
            font-family: {typography['heading_font']};
            font-size: 3.5rem;
            font-weight: 600;
            color: var(--primary);
            margin-bottom: 2rem;
        }}
        
        .section-divider {{
            width: 100px;
            height: 4px;
            background: linear-gradient(90deg, var(--gold), var(--accent));
            margin: 0 auto;
        }}
        
        .about {{
            background: var(--light);
        }}
        
        .about-content {{
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        }}
        
        .about-text {{
            font-size: 1.25rem;
            line-height: 2;
            color: var(--text);
            font-weight: 400;
        }}
        
        .services-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 3rem;
            margin-top: 4rem;
        }}
        
        .service-card {{
            padding: 3rem;
            background: white;
            border-radius: 0;
            text-align: center;
            box-shadow: 0 8px 40px rgba(0, 0, 0, 0.08);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            border-top: 4px solid var(--gold);
        }}
        
        .service-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(201, 176, 55, 0.05), transparent);
            transition: left 0.5s;
        }}
        
        .service-card:hover::before {{
            left: 100%;
        }}
        
        .service-card:hover {{
            transform: translateY(-10px);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        }}
        
        .service-card h3 {{
            font-family: {typography['heading_font']};
            margin-bottom: 1.5rem;
            color: var(--primary);
            font-weight: 600;
            font-size: 1.5rem;
        }}
        
        .service-card p {{
            color: var(--text);
            line-height: 1.8;
            font-size: 1.1rem;
        }}
        
        .contact-section {{
            background: var(--primary);
            color: white;
        }}
        
        .contact-section .section-title {{
            color: white;
        }}
        
        .contact-section .section-divider {{
            background: var(--gold);
        }}
        
        .contact-info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 3rem;
            margin-top: 4rem;
        }}
        
        .contact-item {{
            text-align: center;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 1rem;
            transition: all 0.3s;
        }}
        
        .contact-item:hover {{
            background: rgba(255, 255, 255, 0.1);
            transform: translateY(-5px);
        }}
        
        .contact-item h3 {{
            color: var(--gold);
            font-family: {typography['heading_font']};
            margin-bottom: 1.5rem;
            font-size: 1.4rem;
        }}
        
        .contact-item p {{
            font-size: 1.1rem;
            line-height: 1.6;
        }}
        
        .contact-item a {{
            color: white;
            text-decoration: none;
            transition: color 0.3s;
        }}
        
        .contact-item a:hover {{
            color: var(--gold);
        }}
        
        .footer {{
            background: var(--dark);
            color: white;
            padding: 4rem 0 2rem;
        }}
        
        .footer-content {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 2rem;
        }}
        
        .footer-brand h3 {{
            font-family: {typography['heading_font']};
            font-size: 1.5rem;
            color: var(--gold);
            margin-bottom: 0.5rem;
        }}
        
        .footer-brand p {{
            color: rgba(255, 255, 255, 0.7);
            font-style: italic;
        }}
        
        .footer-info p {{
            color: rgba(255, 255, 255, 0.6);
            font-size: 0.9rem;
        }}
        
        @media (max-width: 768px) {{
            .hero-title {{
                font-size: 2.5rem;
            }}
            
            .hero-subtitle {{
                font-size: 1.1rem;
            }}
            
            .hero-actions {{
                flex-direction: column;
                align-items: center;
            }}
            
            .nav-menu {{
                display: none;
            }}
            
            .services-grid {{
                grid-template-columns: 1fr;
                gap: 2rem;
            }}
            
            .service-card {{
                padding: 2rem;
            }}
            
            .section-title {{
                font-size: 2.5rem;
            }}
            
            .btn {{
                padding: 1rem 2rem;
                font-size: 0.9rem;
            }}
            
            .footer-content {{
                text-align: center;
                flex-direction: column;
            }}
        }}
        """
    
    def _render_services(self, services: list) -> str:
        if not services:
            return ""
        
        service_items = "".join([
            f"""<div class="service-card">
                <h3>{service}</h3>
                <p>Exquisite {service.lower()} delivered with uncompromising attention to detail and luxury standards.</p>
            </div>"""
            for service in services[:6]
        ])
        
        return f"""
        <section id="services" class="section">
            <div class="container">
                <div class="section-header">
                    <h2 class="section-title">Our Premium Services</h2>
                    <div class="section-divider"></div>
                </div>
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
        <section id="contact" class="section contact-section">
            <div class="container">
                <div class="section-header">
                    <h2 class="section-title">Get in Touch</h2>
                    <div class="section-divider"></div>
                </div>
                <div class="contact-info">
                    {f'''<div class="contact-item">
                        <h3>Visit Us</h3>
                        <p>{address}</p>
                    </div>''' if address else ''}
                    {f'''<div class="contact-item">
                        <h3>Call Us</h3>
                        <p><a href="tel:{phone}">{phone}</a></p>
                    </div>''' if phone else ''}
                    <div class="contact-item">
                        <h3>Experience</h3>
                        <p>Luxury service awaits you. Contact us to discover excellence.</p>
                    </div>
                </div>
            </div>
        </section>
        """