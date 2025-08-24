from typing import Dict, Any
from .base_template import BaseTemplate


class ModernTemplate(BaseTemplate):
    def __init__(self):
        super().__init__("Modern", "universal")
        
    def get_structure(self) -> Dict[str, Any]:
        return {
            "sections": [
                "hero",
                "features",
                "about",
                "services",
                "testimonials",
                "contact"
            ],
            "layout": "single-page",
            "navigation": "sticky-transparent"
        }
    
    def get_styles(self) -> Dict[str, Any]:
        return {
            "colors": {
                "primary": "#2563eb",
                "secondary": "#64748b",
                "accent": "#10b981",
                "background": "#ffffff",
                "dark": "#0f172a",
                "light": "#f8fafc"
            },
            "typography": {
                "heading_font": "'Poppins', system-ui, sans-serif",
                "body_font": "'Inter', system-ui, sans-serif",
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
        reviews = business_data.get("reviews", [])
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Modern Business Solutions</title>
    <meta name="description" content="{description or f'{name} - Innovative solutions for your needs'}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@600;700&display=swap" rel="stylesheet">
    <style>
        {self._generate_css()}
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <div class="nav-wrapper">
                <div class="nav-brand">{name}</div>
                <ul class="nav-menu">
                    <li><a href="#home">Home</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#services">Services</a></li>
                    <li><a href="#contact">Contact</a></li>
                </ul>
                <button class="nav-toggle">☰</button>
            </div>
        </div>
    </nav>

    <section id="home" class="hero">
        <div class="hero-bg"></div>
        <div class="container">
            <div class="hero-content">
                <h1 class="hero-title">{name}</h1>
                <p class="hero-subtitle">{description or 'Excellence in Every Detail'}</p>
                <div class="hero-actions">
                    <a href="#services" class="btn btn-primary">Our Services</a>
                    {f'<a href="tel:{phone}" class="btn btn-outline">Call {phone}</a>' if phone else ''}
                </div>
            </div>
        </div>
    </section>

    {self._render_features()}
    
    <section id="about" class="section section-alt">
        <div class="container">
            <div class="section-header">
                <h2>About {name}</h2>
                <p class="section-subtitle">{description or 'Your trusted partner for quality services'}</p>
            </div>
            <div class="about-content">
                <p>{description or f'{name} is committed to delivering exceptional service and building lasting relationships with our clients. Our dedication to quality and customer satisfaction sets us apart.'}</p>
            </div>
        </div>
    </section>

    {self._render_services_modern(services)}
    {self._render_testimonials(reviews)}
    {self._render_contact_modern(business, hours)}
    
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-brand">
                    <h3>{name}</h3>
                    <p>Quality service you can trust</p>
                </div>
                <div class="footer-links">
                    <a href="#services">Services</a>
                    <a href="#about">About</a>
                    <a href="#contact">Contact</a>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 {name}. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script>
        {self._generate_js()}
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
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --primary: {colors['primary']};
            --secondary: {colors['secondary']};
            --accent: {colors['accent']};
            --dark: {colors['dark']};
            --light: {colors['light']};
            --background: {colors['background']};
        }}
        
        body {{
            font-family: {typography['body_font']};
            font-size: {typography['base_size']};
            line-height: 1.6;
            color: var(--dark);
            background: var(--background);
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
            backdrop-filter: blur(10px);
            z-index: 1000;
            padding: 1rem 0;
            transition: all 0.3s;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        
        .nav-wrapper {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .nav-brand {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary);
            font-family: {typography['heading_font']};
        }}
        
        .nav-menu {{
            display: flex;
            list-style: none;
            gap: 2.5rem;
        }}
        
        .nav-menu a {{
            color: var(--dark);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }}
        
        .nav-menu a:hover {{
            color: var(--primary);
        }}
        
        .nav-toggle {{
            display: none;
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
        }}
        
        .hero {{
            padding: calc({spacing['section_padding']} + 80px) 0 {spacing['section_padding']} 0;
            position: relative;
            overflow: hidden;
            min-height: 100vh;
            display: flex;
            align-items: center;
        }}
        
        .hero-bg {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
            opacity: 0.1;
            z-index: -1;
        }}
        
        .hero-content {{
            text-align: center;
            max-width: 800px;
            margin: 0 auto;
        }}
        
        .hero-title {{
            font-size: 4rem;
            margin-bottom: 1.5rem;
            font-family: {typography['heading_font']};
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .hero-subtitle {{
            font-size: 1.5rem;
            margin-bottom: 3rem;
            color: var(--secondary);
            font-weight: 300;
        }}
        
        .hero-actions {{
            display: flex;
            gap: 1.5rem;
            justify-content: center;
        }}
        
        .btn {{
            padding: 1rem 2.5rem;
            border-radius: 50px;
            text-decoration: none;
            display: inline-block;
            font-weight: 600;
            transition: all 0.3s;
            border: 2px solid transparent;
        }}
        
        .btn-primary {{
            background: var(--primary);
            color: white;
            box-shadow: 0 10px 30px rgba(37, 99, 235, 0.3);
        }}
        
        .btn-primary:hover {{
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(37, 99, 235, 0.4);
        }}
        
        .btn-outline {{
            border-color: var(--primary);
            color: var(--primary);
        }}
        
        .btn-outline:hover {{
            background: var(--primary);
            color: white;
        }}
        
        .section {{
            padding: {spacing['section_padding']} 0;
        }}
        
        .section-alt {{
            background: var(--light);
        }}
        
        .section-header {{
            text-align: center;
            margin-bottom: 4rem;
        }}
        
        .section-header h2 {{
            font-size: 3rem;
            margin-bottom: 1rem;
            font-family: {typography['heading_font']};
            color: var(--dark);
        }}
        
        .section-subtitle {{
            font-size: 1.25rem;
            color: var(--secondary);
        }}
        
        .features-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 3rem;
            margin-top: 4rem;
        }}
        
        .feature-card {{
            text-align: center;
            padding: 2rem;
        }}
        
        .feature-icon {{
            width: 60px;
            height: 60px;
            margin: 0 auto 1.5rem;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.5rem;
        }}
        
        .feature-card h3 {{
            margin-bottom: 1rem;
            font-size: 1.5rem;
            color: var(--dark);
        }}
        
        .services-modern {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
            margin-top: 4rem;
        }}
        
        .service-modern {{
            background: white;
            padding: 2.5rem;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.08);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .service-modern:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 50px rgba(0,0,0,0.12);
        }}
        
        .service-modern h3 {{
            color: var(--primary);
            margin-bottom: 1rem;
            font-size: 1.5rem;
        }}
        
        .testimonial-card {{
            background: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            margin: 1rem;
        }}
        
        .testimonial-text {{
            font-style: italic;
            color: var(--secondary);
            margin-bottom: 1rem;
        }}
        
        .testimonial-author {{
            font-weight: 600;
            color: var(--dark);
        }}
        
        .contact-modern {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4rem;
            margin-top: 4rem;
        }}
        
        .contact-info-modern h3 {{
            color: var(--primary);
            margin-bottom: 1.5rem;
            font-size: 1.5rem;
        }}
        
        .hours-table {{
            background: white;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        }}
        
        .hours-table table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .hours-table td {{
            padding: 0.75rem 0;
            border-bottom: 1px solid var(--light);
        }}
        
        .hours-table td:first-child {{
            font-weight: 600;
            color: var(--dark);
        }}
        
        .footer {{
            background: var(--dark);
            color: white;
            padding: 4rem 0 2rem;
            margin-top: 6rem;
        }}
        
        .footer-content {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 4rem;
            margin-bottom: 3rem;
        }}
        
        .footer-brand h3 {{
            margin-bottom: 0.5rem;
            font-size: 1.5rem;
        }}
        
        .footer-links {{
            display: flex;
            gap: 2rem;
            align-items: center;
            justify-content: flex-end;
        }}
        
        .footer-links a {{
            color: rgba(255,255,255,0.7);
            text-decoration: none;
            transition: color 0.3s;
        }}
        
        .footer-links a:hover {{
            color: white;
        }}
        
        .footer-bottom {{
            text-align: center;
            padding-top: 2rem;
            border-top: 1px solid rgba(255,255,255,0.1);
            color: rgba(255,255,255,0.5);
        }}
        
        @media (max-width: 768px) {{
            .nav-menu {{
                display: none;
            }}
            
            .nav-toggle {{
                display: block;
            }}
            
            .hero-title {{
                font-size: 2.5rem;
            }}
            
            .hero-actions {{
                flex-direction: column;
            }}
            
            .contact-modern {{
                grid-template-columns: 1fr;
            }}
            
            .footer-content {{
                grid-template-columns: 1fr;
                text-align: center;
            }}
            
            .footer-links {{
                justify-content: center;
            }}
        }}
        """
    
    def _render_features(self) -> str:
        return """
        <section class="section">
            <div class="container">
                <div class="features-grid">
                    <div class="feature-card">
                        <div class="feature-icon">✨</div>
                        <h3>Quality Service</h3>
                        <p>Committed to excellence in everything we do</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">🤝</div>
                        <h3>Trusted Partner</h3>
                        <p>Building lasting relationships with our clients</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">⚡</div>
                        <h3>Fast & Reliable</h3>
                        <p>Efficient service you can count on</p>
                    </div>
                </div>
            </div>
        </section>
        """
    
    def _render_services_modern(self, services: list) -> str:
        if not services:
            return ""
        
        service_items = "".join([
            f"""<div class="service-modern">
                <h3>{service}</h3>
                <p>Professional {service.lower()} services tailored to your needs</p>
            </div>"""
            for service in services[:6]
        ])
        
        return f"""
        <section id="services" class="section">
            <div class="container">
                <div class="section-header">
                    <h2>Our Services</h2>
                    <p class="section-subtitle">Comprehensive solutions for your needs</p>
                </div>
                <div class="services-modern">
                    {service_items}
                </div>
            </div>
        </section>
        """
    
    def _render_testimonials(self, reviews: list) -> str:
        if not reviews or len(reviews) == 0:
            return ""
        
        review_items = "".join([
            f"""<div class="testimonial-card">
                <p class="testimonial-text">"{review.get('text', 'Great service!')[:200]}"</p>
                <p class="testimonial-author">- {review.get('author', 'Happy Customer')}</p>
            </div>"""
            for review in reviews[:3]
        ])
        
        return f"""
        <section class="section section-alt">
            <div class="container">
                <div class="section-header">
                    <h2>What Our Clients Say</h2>
                    <p class="section-subtitle">Don't just take our word for it</p>
                </div>
                <div class="testimonials-grid">
                    {review_items}
                </div>
            </div>
        </section>
        """
    
    def _render_contact_modern(self, business: Dict[str, Any], hours: Dict[str, str]) -> str:
        address = business.get("address", "")
        phone = business.get("phone", "")
        
        hours_html = ""
        if hours:
            hours_rows = "".join([
                f"<tr><td>{day}</td><td>{time}</td></tr>"
                for day, time in hours.items()
            ])
            hours_html = f"""
            <div class="hours-table">
                <h3>Business Hours</h3>
                <table>
                    {hours_rows}
                </table>
            </div>
            """
        
        return f"""
        <section id="contact" class="section">
            <div class="container">
                <div class="section-header">
                    <h2>Get In Touch</h2>
                    <p class="section-subtitle">We're here to help</p>
                </div>
                <div class="contact-modern">
                    <div class="contact-info-modern">
                        <h3>Contact Information</h3>
                        {f'<p><strong>Address:</strong><br>{address}</p>' if address else ''}
                        {f'<p><strong>Phone:</strong><br><a href="tel:{phone}">{phone}</a></p>' if phone else ''}
                    </div>
                    {hours_html}
                </div>
            </div>
        </section>
        """
    
    def _generate_js(self) -> str:
        return """
        document.querySelector('.nav-toggle').addEventListener('click', function() {
            const menu = document.querySelector('.nav-menu');
            menu.style.display = menu.style.display === 'flex' ? 'none' : 'flex';
        });
        
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
        """