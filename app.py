from flask import Flask, render_template, request, jsonify, session, send_file
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth, firestore
import requests
import json
import os
import uuid
from datetime import datetime
import tempfile
import zipfile

app = Flask(__name__)
app.secret_key = 'ai-website-builder-secret-key-2024'
CORS(app)

# Initialize Firebase with better error handling
try:
    if os.path.exists('firebase-credentials.json'):
        cred = credentials.Certificate('firebase-credentials.json')
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("✅ Firebase initialized with credentials file")
        FIREBASE_ENABLED = True
    else:
        print("⚠️  firebase-credentials.json not found - using mock Firebase")
        FIREBASE_ENABLED = False
        
except Exception as e:
    print(f"❌ Firebase initialization error: {e}")
    FIREBASE_ENABLED = False

# Mock Firebase classes for development
if not FIREBASE_ENABLED:
    class MockFirestore:
        def collection(self, name):
            return MockCollection()
    
    class MockCollection:
        def document(self, doc_id):
            return MockDocument()
        def where(self, field, op, value):
            return MockQuery()
        def add(self, data):
            return MockDocument()
            
    class MockQuery:
        def order_by(self, field, direction=None):
            return self
        def stream(self):
            return []
            
    class MockDocument:
        def set(self, data):
            pass
        def get(self):
            return MockDocSnapshot()
        def delete(self):
            pass
        def to_dict(self):
            return {}
            
    class MockDocSnapshot:
        def exists(self):
            return False
        def to_dict(self):
            return {}
    
    db = MockFirestore()

# API Keys - Updated with correct model names
GEMINI_API_KEY = "AIzaSyCYcgTGH82oRTPi4ALavKR7HHw46n0fiqI"
HUGGING_FACE_TOKEN = "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"
GROQ_API_KEY = "gsk_XFabGnrgpSx6IPPQza4SWGdyb3FYjFwEpAG7ZhM0BXvsaT9VPPOCFirebase"

def generate_premium_website(prompt):
    """Generate a premium website with ultra-modern design"""
    title = extract_title_from_prompt(prompt)
    website_type = determine_website_type(prompt)
    
    if website_type == "portfolio":
        return generate_portfolio_template(prompt, title)
    elif website_type == "business":
        return generate_business_template(prompt, title)
    elif website_type == "restaurant":
        return generate_restaurant_template(prompt, title)
    elif website_type == "ecommerce":
        return generate_ecommerce_template(prompt, title)
    else:
        return generate_ultra_modern_template(prompt, title)

def generate_ultra_modern_template(prompt, title):
    """Generate an ultra-modern, glassmorphism website template"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {{
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --secondary: #ec4899;
            --accent: #06b6d4;
            --success: #10b981;
            --warning: #f59e0b;
            --text: #1e293b;
            --text-light: #64748b;
            --text-lighter: #94a3b8;
            --bg: #ffffff;
            --bg-alt: #f8fafc;
            --glass: rgba(255, 255, 255, 0.25);
            --glass-border: rgba(255, 255, 255, 0.18);
            --shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            --shadow-lg: 0 25px 50px rgba(31, 38, 135, 0.5);
            --gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-2: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --gradient-3: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            --gradient-4: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.6;
            color: var(--text);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            overflow-x: hidden;
        }}

        /* Animated Background */
        .bg-animation {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}

        .bg-animation::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: radial-gradient(circle at 30% 20%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
                        radial-gradient(circle at 70% 80%, rgba(118, 75, 162, 0.1) 0%, transparent 50%);
            animation: float 20s ease-in-out infinite;
        }}

        @keyframes float {{
            0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
            33% {{ transform: translateY(-30px) rotate(1deg); }}
            66% {{ transform: translateY(-20px) rotate(-1deg); }}
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }}

        /* Glassmorphism Header */
        header {{
            position: fixed;
            top: 0;
            width: 100%;
            background: var(--glass);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--glass-border);
            z-index: 1000;
            transition: all 0.3s ease;
        }}

        nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }}

        .logo {{
            font-family: 'Poppins', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
        }}

        .nav-links {{
            display: flex;
            list-style: none;
            gap: 2rem;
            align-items: center;
        }}

        .nav-links a {{
            text-decoration: none;
            color: white;
            font-weight: 500;
            transition: all 0.3s ease;
            position: relative;
            padding: 0.5rem 1rem;
            border-radius: 50px;
        }}

        .nav-links a:hover {{
            background: var(--glass);
            backdrop-filter: blur(10px);
            transform: translateY(-2px);
        }}

        .cta-btn {{
            background: var(--glass);
            backdrop-filter: blur(20px);
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            border: 1px solid var(--glass-border);
            box-shadow: var(--shadow);
        }}

        .cta-btn:hover {{
            transform: translateY(-3px);
            box-shadow: var(--shadow-lg);
            background: rgba(255, 255, 255, 0.3);
        }}

        /* Hero Section with Glassmorphism */
        .hero {{
            min-height: 100vh;
            display: flex;
            align-items: center;
            position: relative;
            overflow: hidden;
        }}

        .hero-content {{
            position: relative;
            z-index: 2;
            max-width: 800px;
            text-align: center;
            margin: 0 auto;
        }}

        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 50px;
            color: white;
            font-size: 0.9rem;
            font-weight: 500;
            margin-bottom: 2rem;
            animation: fadeInUp 0.8s ease;
        }}

        .hero h1 {{
            font-family: 'Poppins', sans-serif;
            font-size: clamp(3rem, 6vw, 5rem);
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 1.5rem;
            color: white;
            text-shadow: 0 0 50px rgba(255, 255, 255, 0.3);
            animation: fadeInUp 0.8s ease 0.2s both;
        }}

        .hero .gradient-text {{
            background: var(--gradient-3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .hero p {{
            font-size: 1.3rem;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 2.5rem;
            line-height: 1.6;
            animation: fadeInUp 0.8s ease 0.4s both;
        }}

        .hero-buttons {{
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
            animation: fadeInUp 0.8s ease 0.6s both;
        }}

        .btn {{
            padding: 1rem 2rem;
            border-radius: 50px;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            border: none;
            cursor: pointer;
            font-size: 1rem;
            position: relative;
            overflow: hidden;
        }}

        .btn::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s ease;
        }}

        .btn:hover::before {{
            left: 100%;
        }}

        .btn-primary {{
            background: var(--glass);
            backdrop-filter: blur(20px);
            color: white;
            border: 1px solid var(--glass-border);
            box-shadow: var(--shadow);
        }}

        .btn-primary:hover {{
            transform: translateY(-3px);
            box-shadow: var(--shadow-lg);
            background: rgba(255, 255, 255, 0.3);
        }}

        .btn-secondary {{
            background: transparent;
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.3);
        }}

        .btn-secondary:hover {{
            background: var(--glass);
            backdrop-filter: blur(20px);
            transform: translateY(-3px);
        }}

        /* Floating Cards Section */
        .features {{
            padding: 8rem 0;
            position: relative;
        }}

        .section-header {{
            text-align: center;
            margin-bottom: 4rem;
        }}

        .section-header h2 {{
            font-family: 'Poppins', sans-serif;
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: white;
            text-shadow: 0 0 30px rgba(255, 255, 255, 0.3);
        }}

        .section-header p {{
            font-size: 1.3rem;
            color: rgba(255, 255, 255, 0.8);
            max-width: 600px;
            margin: 0 auto;
        }}

        .features-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
            perspective: 1000px;
        }}

        .feature-card {{
            background: var(--glass);
            backdrop-filter: blur(20px);
            padding: 2.5rem;
            border-radius: 20px;
            border: 1px solid var(--glass-border);
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}

        .feature-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: var(--gradient-1);
        }}

        .feature-card:hover {{
            transform: translateY(-10px) rotateX(5deg);
            box-shadow: var(--shadow-lg);
        }}

        .feature-icon {{
            width: 70px;
            height: 70px;
            background: var(--gradient-1);
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1.5rem;
            color: white;
            font-size: 1.8rem;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }}

        .feature-card:nth-child(2) .feature-icon {{
            background: var(--gradient-2);
            box-shadow: 0 10px 30px rgba(240, 147, 251, 0.3);
        }}

        .feature-card:nth-child(3) .feature-icon {{
            background: var(--gradient-3);
            box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);
        }}

        .feature-card h3 {{
            font-family: 'Poppins', sans-serif;
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: white;
        }}

        .feature-card p {{
            color: rgba(255, 255, 255, 0.8);
            line-height: 1.6;
        }}

        /* Stats with Counter Animation */
        .stats {{
            padding: 4rem 0;
            background: var(--glass);
            backdrop-filter: blur(20px);
            border-top: 1px solid var(--glass-border);
            border-bottom: 1px solid var(--glass-border);
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            text-align: center;
        }}

        .stat-item {{
            padding: 1rem;
        }}

        .stat-item h3 {{
            font-family: 'Poppins', sans-serif;
            font-size: 3.5rem;
            font-weight: 800;
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
        }}

        .stat-item p {{
            color: rgba(255, 255, 255, 0.8);
            font-weight: 500;
            font-size: 1.1rem;
        }}

        /* Footer */
        footer {{
            background: rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(20px);
            color: white;
            padding: 3rem 0 1rem;
            border-top: 1px solid var(--glass-border);
        }}

        .footer-content {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }}

        .footer-section h3 {{
            font-family: 'Poppins', sans-serif;
            margin-bottom: 1rem;
            color: white;
            font-weight: 600;
        }}

        .footer-section p,
        .footer-section a {{
            color: rgba(255, 255, 255, 0.7);
            text-decoration: none;
            line-height: 1.8;
            transition: color 0.3s ease;
        }}

        .footer-section a:hover {{
            color: white;
        }}

        .footer-bottom {{
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            padding-top: 1rem;
            text-align: center;
            color: rgba(255, 255, 255, 0.6);
        }}

        /* Animations */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(50px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .feature-card {{
            animation: fadeInUp 0.8s ease forwards;
        }}

        .feature-card:nth-child(2) {{
            animation-delay: 0.2s;
        }}

        .feature-card:nth-child(3) {{
            animation-delay: 0.4s;
        }}

        /* Mobile Responsive */
        @media (max-width: 768px) {{
            .nav-links {{
                display: none;
            }}
            
            .hero-buttons {{
                flex-direction: column;
                align-items: center;
            }}
            
            .btn {{
                width: 100%;
                max-width: 300px;
                justify-content: center;
            }}
            
            .features-grid {{
                grid-template-columns: 1fr;
            }}
            
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .section-header h2 {{
                font-size: 2rem;
            }}
        }}

        /* Scroll Animations */
        .scroll-reveal {{
            opacity: 0;
            transform: translateY(50px);
            transition: all 0.8s ease;
        }}

        .scroll-reveal.revealed {{
            opacity: 1;
            transform: translateY(0);
        }}
    </style>
</head>
<body>
    <div class="bg-animation"></div>
    
    <header>
        <nav>
            <div class="logo">{title}</div>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#features">Features</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
                <li><a href="#contact" class="cta-btn">Get Started</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <section class="hero" id="home">
            <div class="container">
                <div class="hero-content">
                    <div class="hero-badge">
                        <i class="fas fa-sparkles"></i>
                        <span>AI Generated Excellence</span>
                    </div>
                    <h1>Welcome to <span class="gradient-text">{title}</span></h1>
                    <p>Experience the future with this stunning website created by advanced AI. Built with modern design principles, glassmorphism effects, and cutting-edge technology based on your vision: "{prompt}"</p>
                    <div class="hero-buttons">
                        <a href="#features" class="btn btn-primary">
                            <i class="fas fa-rocket"></i>
                            Explore Features
                        </a>
                        <a href="#contact" class="btn btn-secondary">
                            <i class="fas fa-phone"></i>
                            Get in Touch
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <section class="features" id="features">
            <div class="container">
                <div class="section-header scroll-reveal">
                    <h2>Incredible Features</h2>
                    <p>Discover the cutting-edge capabilities that set us apart from the competition</p>
                </div>
                <div class="features-grid">
                    <div class="feature-card scroll-reveal">
                        <div class="feature-icon">
                            <i class="fas fa-bolt"></i>
                        </div>
                        <h3>Lightning Performance</h3>
                        <p>Experience unprecedented speed with our optimized architecture, delivering content at the speed of light with zero compromise on quality.</p>
                    </div>
                    <div class="feature-card scroll-reveal">
                        <div class="feature-icon">
                            <i class="fas fa-shield-alt"></i>
                        </div>
                        <h3>Fort Knox Security</h3>
                        <p>Your data is protected by military-grade encryption and advanced security protocols, ensuring complete privacy and peace of mind.</p>
                    </div>
                    <div class="feature-card scroll-reveal">
                        <div class="feature-icon">
                            <i class="fas fa-magic"></i>
                        </div>
                        <h3>AI-Powered Intelligence</h3>
                        <p>Harness the power of artificial intelligence to automate complex tasks and provide intelligent insights that drive your success.</p>
                    </div>
                </div>
            </div>
        </section>

        <section class="stats">
            <div class="container">
                <div class="stats-grid">
                    <div class="stat-item">
                        <h3 class="counter" data-target="50000">0</h3>
                        <p>Happy Customers</p>
                    </div>
                    <div class="stat-item">
                        <h3 class="counter" data-target="99.9">0</h3>
                        <p>% Uptime</p>
                    </div>
                    <div class="stat-item">
                        <h3 class="counter" data-target="24">0</h3>
                        <p>Hour Support</p>
                    </div>
                    <div class="stat-item">
                        <h3 class="counter" data-target="150">0</h3>
                        <p>Countries Served</p>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <footer id="contact">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>{title}</h3>
                    <p>Pioneering the future with innovative AI-powered solutions. Join our community of forward-thinking individuals and businesses.</p>
                </div>
                <div class="footer-section">
                    <h3>Quick Links</h3>
                    <p><a href="#home">Home</a></p>
                    <p><a href="#features">Features</a></p>
                    <p><a href="#about">About</a></p>
                    <p><a href="#contact">Contact</a></p>
                </div>
                <div class="footer-section">
                    <h3>Get in Touch</h3>
                    <p><i class="fas fa-envelope"></i> hello@{title.lower().replace(' ', '')}.com</p>
                    <p><i class="fas fa-phone"></i> +1 (555) 123-4567</p>
                    <p><i class="fas fa-map-marker-alt"></i> 123 Innovation Drive, Tech City</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 {title}. All rights reserved. | Crafted with AI Excellence</p>
            </div>
        </div>
    </footer>

    <script>
        // Smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});
                }}
            }});
        }});

        // Header scroll effect
        window.addEventListener('scroll', () => {{
            const header = document.querySelector('header');
            if (window.scrollY > 100) {{
                header.style.background = 'rgba(255, 255, 255, 0.1)';
                header.style.backdropFilter = 'blur(30px)';
            }} else {{
                header.style.background = 'rgba(255, 255, 255, 0.25)';
                header.style.backdropFilter = 'blur(20px)';
            }}
        }});

        // Scroll reveal animation
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }};

        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('revealed');
                }}
            }});
        }}, observerOptions);

        document.querySelectorAll('.scroll-reveal').forEach(el => {{
            observer.observe(el);
        }});

        // Counter animation
        const counters = document.querySelectorAll('.counter');
        const counterObserver = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    const counter = entry.target;
                    const target = parseInt(counter.dataset.target);
                    const increment = target / 100;
                    let current = 0;
                    
                    const updateCounter = () => {{
                        if (current < target) {{
                            current += increment;
                            if (target === 99.9) {{
                                counter.textContent = current.toFixed(1);
                            }} else {{
                                counter.textContent = Math.floor(current).toLocaleString();
                            }}
                            requestAnimationFrame(updateCounter);
                        }} else {{
                            if (target === 99.9) {{
                                counter.textContent = '99.9';
                            }} else {{
                                counter.textContent = target.toLocaleString();
                            }}
                        }}
                    }};
                    
                    updateCounter();
                    counterObserver.unobserve(counter);
                }}
            }});
        }}, {{ threshold: 0.5 }});

        counters.forEach(counter => {{
            counterObserver.observe(counter);
        }});

        // Parallax effect for hero
        window.addEventListener('scroll', () => {{
            const scrolled = window.pageYOffset;
            const hero = document.querySelector('.hero');
            if (hero) {{
                hero.style.transform = `translateY(${{scrolled * 0.5}}px)`;
            }}
        }});
    </script>
</body>
</html>"""

def generate_portfolio_template(prompt, title):
    """Generate a stunning portfolio template"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Creative Portfolio</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {{
            --primary: #6366f1;
            --secondary: #8b5cf6;
            --accent: #06b6d4;
            --dark: #0f172a;
            --light: #f8fafc;
            --glass: rgba(255, 255, 255, 0.1);
            --glass-border: rgba(255, 255, 255, 0.2);
            --gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-2: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --gradient-3: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            --shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', sans-serif;
            background: var(--dark);
            color: white;
            overflow-x: hidden;
        }}

        /* Animated Background */
        .bg-animation {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: linear-gradient(45deg, #0f172a, #1e293b, #334155);
            background-size: 400% 400%;
            animation: gradientShift 15s ease infinite;
        }}

        @keyframes gradientShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        /* Navigation */
        nav {{
            position: fixed;
            top: 0;
            width: 100%;
            padding: 1rem 2rem;
            background: var(--glass);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--glass-border);
            z-index: 1000;
        }}

        .nav-container {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo {{
            font-family: 'Playfair Display', serif;
            font-size: 1.8rem;
            font-weight: 700;
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .nav-links {{
            display: flex;
            list-style: none;
            gap: 2rem;
        }}

        .nav-links a {{
            color: white;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s ease;
            position: relative;
        }}

        .nav-links a::after {{
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 0;
            height: 2px;
            background: var(--gradient-1);
            transition: width 0.3s ease;
        }}

        .nav-links a:hover::after {{
            width: 100%;
        }}

        /* Hero Section */
        .hero {{
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            position: relative;
        }}

        .hero-content {{
            max-width: 800px;
            padding: 0 2rem;
        }}

        .hero h1 {{
            font-family: 'Playfair Display', serif;
            font-size: clamp(3rem, 6vw, 6rem);
            font-weight: 700;
            margin-bottom: 1.5rem;
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: fadeInUp 1s ease;
        }}

        .hero p {{
            font-size: 1.3rem;
            color: rgba(255, 255, 255, 0.8);
            margin-bottom: 2rem;
            animation: fadeInUp 1s ease 0.2s both;
        }}

        .hero-buttons {{
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
            animation: fadeInUp 1s ease 0.4s both;
        }}

        .btn {{
            padding: 1rem 2rem;
            border: none;
            border-radius: 50px;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }}

        .btn-primary {{
            background: var(--gradient-1);
            color: white;
        }}

        .btn-outline {{
            background: transparent;
            color: white;
            border: 2px solid var(--glass-border);
        }}

        .btn:hover {{
            transform: translateY(-3px);
            box-shadow: var(--shadow);
        }}

        /* Portfolio Grid */
        .portfolio {{
            padding: 6rem 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }}

        .section-title {{
            font-family: 'Playfair Display', serif;
            font-size: 3rem;
            text-align: center;
            margin-bottom: 3rem;
            background: var(--gradient-2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .portfolio-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
        }}

        .portfolio-item {{
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            overflow: hidden;
            transition: all 0.3s ease;
            cursor: pointer;
        }}

        .portfolio-item:hover {{
            transform: translateY(-10px);
            box-shadow: var(--shadow);
        }}

        .portfolio-image {{
            height: 250px;
            background: var(--gradient-3);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3rem;
            color: white;
        }}

        .portfolio-content {{
            padding: 1.5rem;
        }}

        .portfolio-content h3 {{
            font-size: 1.3rem;
            margin-bottom: 0.5rem;
            color: white;
        }}

        .portfolio-content p {{
            color: rgba(255, 255, 255, 0.7);
            line-height: 1.6;
        }}

        /* Skills Section */
        .skills {{
            padding: 6rem 2rem;
            background: var(--glass);
            backdrop-filter: blur(20px);
        }}

        .skills-container {{
            max-width: 1200px;
            margin: 0 auto;
        }}

        .skills-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }}

        .skill-item {{
            text-align: center;
            padding: 2rem;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            border: 1px solid var(--glass-border);
        }}

        .skill-icon {{
            font-size: 3rem;
            margin-bottom: 1rem;
            background: var(--gradient-1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .skill-item h3 {{
            margin-bottom: 0.5rem;
            color: white;
        }}

        .skill-item p {{
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9rem;
        }}

        /* Contact Section */
        .contact {{
            padding: 6rem 2rem;
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        }}

        .contact-form {{
            display: grid;
            gap: 1.5rem;
            margin-top: 3rem;
        }}

        .form-group {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }}

        .form-group.full {{
            grid-template-columns: 1fr;
        }}

        .contact-form input,
        .contact-form textarea {{
            padding: 1rem;
            border: 1px solid var(--glass-border);
            border-radius: 10px;
            background: var(--glass);
            backdrop-filter: blur(20px);
            color: white;
            font-family: inherit;
        }}

        .contact-form input::placeholder,
        .contact-form textarea::placeholder {{
            color: rgba(255, 255, 255, 0.5);
        }}

        /* Animations */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(50px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .nav-links {{
                display: none;
            }}
            
            .hero-buttons {{
                flex-direction: column;
                align-items: center;
            }}
            
            .btn {{
                width: 100%;
                max-width: 300px;
            }}
            
            .form-group {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="bg-animation"></div>
    
    <nav>
        <div class="nav-container">
            <div class="logo">{title}</div>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#portfolio">Portfolio</a></li>
                <li><a href="#skills">Skills</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </div>
    </nav>

    <section class="hero" id="home">
        <div class="hero-content">
            <h1>Creative Portfolio</h1>
            <p>Welcome to my creative world. This stunning portfolio was generated by AI based on your vision: "{prompt}"</p>
            <div class="hero-buttons">
                <a href="#portfolio" class="btn btn-primary">View My Work</a>
                <a href="#contact" class="btn btn-outline">Get In Touch</a>
            </div>
        </div>
    </section>

    <section class="portfolio" id="portfolio">
        <h2 class="section-title">My Portfolio</h2>
        <div class="portfolio-grid">
            <div class="portfolio-item">
                <div class="portfolio-image">
                    <i class="fas fa-camera"></i>
                </div>
                <div class="portfolio-content">
                    <h3>Photography Project</h3>
                    <p>A stunning collection of landscape and portrait photography showcasing natural beauty.</p>
                </div>
            </div>
            <div class="portfolio-item">
                <div class="portfolio-image">
                    <i class="fas fa-paint-brush"></i>
                </div>
                <div class="portfolio-content">
                    <h3>Design Work</h3>
                    <p>Creative design solutions for modern brands and digital experiences.</p>
                </div>
            </div>
            <div class="portfolio-item">
                <div class="portfolio-image">
                    <i class="fas fa-code"></i>
                </div>
                <div class="portfolio-content">
                    <h3>Web Development</h3>
                    <p>Modern, responsive websites built with cutting-edge technologies.</p>
                </div>
            </div>
        </div>
    </section>

    <section class="skills" id="skills">
        <div class="skills-container">
            <h2 class="section-title">My Skills</h2>
            <div class="skills-grid">
                <div class="skill-item">
                    <div class="skill-icon">
                        <i class="fas fa-palette"></i>
                    </div>
                    <h3>Creative Design</h3>
                    <p>Visual design and branding</p>
                </div>
                <div class="skill-item">
                    <div class="skill-icon">
                        <i class="fas fa-laptop-code"></i>
                    </div>
                    <h3>Development</h3>
                    <p>Frontend and backend coding</p>
                </div>
                <div class="skill-item">
                    <div class="skill-icon">
                        <i class="fas fa-mobile-alt"></i>
                    </div>
                    <h3>Mobile Design</h3>
                    <p>Responsive and mobile-first</p>
                </div>
                <div class="skill-item">
                    <div class="skill-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <h3>Strategy</h3>
                    <p>Digital marketing and growth</p>
                </div>
            </div>
        </div>
    </section>

    <section class="contact" id="contact">
        <h2 class="section-title">Let's Work Together</h2>
        <p>Ready to bring your ideas to life? Let's create something amazing together.</p>
        <form class="contact-form">
            <div class="form-group">
                <input type="text" placeholder="Your Name" required>
                <input type="email" placeholder="Your Email" required>
            </div>
            <div class="form-group full">
                <input type="text" placeholder="Subject" required>
            </div>
            <div class="form-group full">
                <textarea rows="5" placeholder="Your Message" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary">Send Message</button>
        </form>
    </section>

    <script>
        // Smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});

        // Scroll animations
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }};

        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }}
            }});
        }}, observerOptions);

        document.querySelectorAll('.portfolio-item, .skill-item').forEach(el => {{
            el.style.opacity = '0';
            el.style.transform = 'translateY(50px)';
            el.style.transition = 'all 0.8s ease';
            observer.observe(el);
        }});

        // Form submission
        document.querySelector('.contact-form').addEventListener('submit', function(e) {{
            e.preventDefault();
            alert('Thank you for your message! I\\'ll get back to you soon.');
        }});
    </script>
</body>
</html>"""

def generate_business_template(prompt, title):
    """Generate a professional business template"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Professional Business</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {{
            --primary: #2563eb;
            --secondary: #1e40af;
            --accent: #3b82f6;
            --success: #059669;
            --warning: #d97706;
            --dark: #1e293b;
            --light: #f8fafc;
            --white: #ffffff;
            --gray-100: #f1f5f9;
            --gray-200: #e2e8f0;
            --gray-300: #cbd5e1;
            --gray-600: #475569;
            --gray-800: #1e293b;
            --gradient-1: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --gradient-2: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
            --shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 25px 50px rgba(0, 0, 0, 0.15);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: var(--gray-800);
            background: var(--white);
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }}

        /* Header */
        header {{
            position: fixed;
            top: 0;
            width: 100%;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--gray-200);
            z-index: 1000;
            transition: all 0.3s ease;
        }}

        nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }}

        .logo {{
            font-family: 'Poppins', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--primary);
        }}

        .nav-links {{
            display: flex;
            list-style: none;
            gap: 2rem;
            align-items: center;
        }}

        .nav-links a {{
            text-decoration: none;
            color: var(--gray-600);
            font-weight: 500;
            transition: all 0.3s ease;
            position: relative;
        }}

        .nav-links a:hover {{
            color: var(--primary);
        }}

        .nav-links a::after {{
            content: '';
            position: absolute;
            bottom: -5px;
            left: 0;
            width: 0;
            height: 2px;
            background: var(--primary);
            transition: width 0.3s ease;
        }}

        .nav-links a:hover::after {{
            width: 100%;
        }}

        .cta-btn {{
            background: var(--primary);
            color: white;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: var(--shadow);
        }}

        .cta-btn:hover {{
            background: var(--secondary);
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }}

        /* Hero Section */
        .hero {{
            min-height: 100vh;
            display: flex;
            align-items: center;
            background: linear-gradient(135deg, var(--light) 0%, var(--gray-100) 100%);
            position: relative;
            overflow: hidden;
        }}

        .hero::before {{
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 50%;
            height: 100%;
            background: var(--gradient-1);
            clip-path: polygon(30% 0%, 100% 0%, 100% 100%, 0% 100%);
            opacity: 0.1;
        }}

        .hero-content {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4rem;
            align-items: center;
            position: relative;
            z-index: 2;
        }}

        .hero-text h1 {{
            font-family: 'Poppins', sans-serif;
            font-size: clamp(2.5rem, 5vw, 4rem);
            font-weight: 700;
            line-height: 1.1;
            margin-bottom: 1.5rem;
            color: var(--gray-800);
        }}

        .hero-text .highlight {{
            color: var(--primary);
        }}

        .hero-text p {{
            font-size: 1.2rem;
            color: var(--gray-600);
            margin-bottom: 2rem;
            line-height: 1.6;
        }}

        .hero-buttons {{
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }}

        .btn {{
            padding: 1rem 2rem;
            border-radius: 8px;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            border: none;
            cursor: pointer;
            font-size: 1rem;
        }}

        .btn-primary {{
            background: var(--primary);
            color: white;
            box-shadow: var(--shadow);
        }}

        .btn-primary:hover {{
            background: var(--secondary);
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }}

        .btn-outline {{
            background: transparent;
            color: var(--primary);
            border: 2px solid var(--primary);
        }}

        .btn-outline:hover {{
            background: var(--primary);
            color: white;
        }}

        .hero-image {{
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .hero-placeholder {{
            width: 400px;
            height: 300px;
            background: var(--gradient-1);
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 4rem;
            box-shadow: var(--shadow-lg);
            animation: float 6s ease-in-out infinite;
        }}

        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-20px); }}
        }}

        /* Services Section */
        .services {{
            padding: 6rem 0;
            background: var(--white);
        }}

        .section-header {{
            text-align: center;
            margin-bottom: 4rem;
        }}

        .section-header h2 {{
            font-family: 'Poppins', sans-serif;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: var(--gray-800);
        }}

        .section-header p {{
            font-size: 1.2rem;
            color: var(--gray-600);
            max-width: 600px;
            margin: 0 auto;
        }}

        .services-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }}

        .service-card {{
            background: var(--white);
            padding: 2.5rem;
            border-radius: 15px;
            box-shadow: var(--shadow);
            transition: all 0.3s ease;
            border: 1px solid var(--gray-200);
        }}

        .service-card:hover {{
            transform: translateY(-10px);
            box-shadow: var(--shadow-lg);
        }}

        .service-icon {{
            width: 70px;
            height: 70px;
            background: var(--gradient-2);
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 1.5rem;
            color: white;
            font-size: 1.8rem;
        }}

        .service-card h3 {{
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--gray-800);
        }}

        .service-card p {{
            color: var(--gray-600);
            line-height: 1.6;
        }}

        /* Stats Section */
        .stats {{
            padding: 4rem 0;
            background: var(--gray-800);
            color: white;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 2rem;
            text-align: center;
        }}

        .stat-item h3 {{
            font-size: 3rem;
            font-weight: 800;
            color: var(--primary);
            margin-bottom: 0.5rem;
        }}

        .stat-item p {{
            font-size: 1.1rem;
            color: var(--gray-300);
        }}

        /* Contact Section */
        .contact {{
            padding: 6rem 0;
            background: var(--light);
        }}

        .contact-content {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4rem;
            align-items: start;
        }}

        .contact-info h3 {{
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--gray-800);
        }}

        .contact-info p {{
            color: var(--gray-600);
            margin-bottom: 2rem;
        }}

        .contact-item {{
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }}

        .contact-item i {{
            width: 40px;
            height: 40px;
            background: var(--primary);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .contact-form {{
            background: var(--white);
            padding: 2.5rem;
            border-radius: 15px;
            box-shadow: var(--shadow);
        }}

        .form-group {{
            margin-bottom: 1.5rem;
        }}

        .form-group label {{
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: var(--gray-800);
        }}

        .form-group input,
        .form-group textarea {{
            width: 100%;
            padding: 1rem;
            border: 2px solid var(--gray-200);
            border-radius: 8px;
            font-family: inherit;
            transition: border-color 0.3s ease;
        }}

        .form-group input:focus,
        .form-group textarea:focus {{
            outline: none;
            border-color: var(--primary);
        }}

        /* Footer */
        footer {{
            background: var(--gray-800);
            color: white;
            padding: 3rem 0 1rem;
        }}

        .footer-content {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }}

        .footer-section h3 {{
            margin-bottom: 1rem;
            color: white;
        }}

        .footer-section p,
        .footer-section a {{
            color: var(--gray-300);
            text-decoration: none;
            line-height: 1.8;
        }}

        .footer-section a:hover {{
            color: var(--primary);
        }}

        .footer-bottom {{
            border-top: 1px solid var(--gray-600);
            padding-top: 1rem;
            text-align: center;
            color: var(--gray-300);
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .nav-links {{
                display: none;
            }}
            
            .hero-content {{
                grid-template-columns: 1fr;
                text-align: center;
            }}
            
            .contact-content {{
                grid-template-columns: 1fr;
            }}
            
            .hero-placeholder {{
                width: 300px;
                height: 200px;
                font-size: 3rem;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <nav>
            <div class="logo">{title}</div>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#services">Services</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
                <li><a href="#contact" class="cta-btn">Get Started</a></li>
            </ul>
        </nav>
    </header>

    <section class="hero" id="home">
        <div class="container">
            <div class="hero-content">
                <div class="hero-text">
                    <h1>Professional <span class="highlight">Business Solutions</span></h1>
                    <p>Transform your business with our innovative solutions. This professional website was created by AI based on your vision: "{prompt}"</p>
                    <div class="hero-buttons">
                        <a href="#services" class="btn btn-primary">
                            <i class="fas fa-rocket"></i>
                            Our Services
                        </a>
                        <a href="#contact" class="btn btn-outline">
                            <i class="fas fa-phone"></i>
                            Contact Us
                        </a>
                    </div>
                </div>
                <div class="hero-image">
                    <div class="hero-placeholder">
                        <i class="fas fa-building"></i>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="services" id="services">
        <div class="container">
            <div class="section-header">
                <h2>Our Services</h2>
                <p>We provide comprehensive business solutions to help your company thrive in today's competitive market</p>
            </div>
            <div class="services-grid">
                <div class="service-card">
                    <div class="service-icon">
                        <i class="fas fa-chart-line"></i>
                    </div>
                    <h3>Business Strategy</h3>
                    <p>Strategic planning and consulting to drive your business forward with data-driven insights and proven methodologies.</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">
                        <i class="fas fa-laptop-code"></i>
                    </div>
                    <h3>Digital Solutions</h3>
                    <p>Custom software development and digital transformation services to modernize your business operations.</p>
                </div>
                <div class="service-card">
                    <div class="service-icon">
                        <i class="fas fa-users"></i>
                    </div>
                    <h3>Team Development</h3>
                    <p>Professional training and development programs to enhance your team's skills and productivity.</p>
                </div>
            </div>
        </div>
    </section>

    <section class="stats">
        <div class="container">
            <div class="stats-grid">
                <div class="stat-item">
                    <h3>500+</h3>
                    <p>Happy Clients</p>
                </div>
                <div class="stat-item">
                    <h3>1000+</h3>
                    <p>Projects Completed</p>
                </div>
                <div class="stat-item">
                    <h3>15+</h3>
                    <p>Years Experience</p>
                </div>
                <div class="stat-item">
                    <h3>24/7</h3>
                    <p>Support Available</p>
                </div>
            </div>
        </div>
    </section>

    <section class="contact" id="contact">
        <div class="container">
            <div class="section-header">
                <h2>Get In Touch</h2>
                <p>Ready to take your business to the next level? Contact us today for a free consultation</p>
            </div>
            <div class="contact-content">
                <div class="contact-info">
                    <h3>Contact Information</h3>
                    <p>We're here to help you succeed. Reach out to us through any of these channels.</p>
                    <div class="contact-item">
                        <i class="fas fa-map-marker-alt"></i>
                        <div>
                            <strong>Address</strong><br>
                            123 Business Ave, Suite 100<br>
                            City, State 12345
                        </div>
                    </div>
                    <div class="contact-item">
                        <i class="fas fa-phone"></i>
                        <div>
                            <strong>Phone</strong><br>
                            +1 (555) 123-4567
                        </div>
                    </div>
                    <div class="contact-item">
                        <i class="fas fa-envelope"></i>
                        <div>
                            <strong>Email</strong><br>
                            info@{title.lower().replace(' ', '')}.com
                        </div>
                    </div>
                </div>
                <form class="contact-form">
                    <div class="form-group">
                        <label for="name">Full Name</label>
                        <input type="text" id="name" required>
                    </div>
                    <div class="form-group">
                        <label for="email">Email Address</label>
                        <input type="email" id="email" required>
                    </div>
                    <div class="form-group">
                        <label for="subject">Subject</label>
                        <input type="text" id="subject" required>
                    </div>
                    <div class="form-group">
                        <label for="message">Message</label>
                        <textarea id="message" rows="5" required></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">
                        <i class="fas fa-paper-plane"></i>
                        Send Message
                    </button>
                </form>
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>{title}</h3>
                    <p>Your trusted partner for professional business solutions and digital transformation.</p>
                </div>
                <div class="footer-section">
                    <h3>Services</h3>
                    <p><a href="#services">Business Strategy</a></p>
                    <p><a href="#services">Digital Solutions</a></p>
                    <p><a href="#services">Team Development</a></p>
                </div>
                <div class="footer-section">
                    <h3>Company</h3>
                    <p><a href="#about">About Us</a></p>
                    <p><a href="#contact">Contact</a></p>
                    <p><a href="#">Privacy Policy</a></p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 {title}. All rights reserved. | Powered by AI Excellence</p>
            </div>
        </div>
    </footer>

    <script>
        // Smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({{
                    behavior: 'smooth'
                }});
            }});
        }});

        // Header scroll effect
        window.addEventListener('scroll', () => {{
            const header = document.querySelector('header');
            if (window.scrollY > 100) {{
                header.style.background = 'rgba(255, 255, 255, 0.98)';
                header.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
            }} else {{
                header.style.background = 'rgba(255, 255, 255, 0.95)';
                header.style.boxShadow = 'none';
            }}
        }});

        // Form submission
        document.querySelector('.contact-form').addEventListener('submit', function(e) {{
            e.preventDefault();
            alert('Thank you for your message! We\\'ll get back to you soon.');
        }});

        // Counter animation for stats
        const stats = document.querySelectorAll('.stat-item h3');
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    const target = entry.target;
                    const text = target.textContent;
                    const number = parseInt(text.replace(/[^0-9]/g, ''));
                    if (number) {{
                        let current = 0;
                        const increment = number / 50;
                        const timer = setInterval(() => {{
                            current += increment;
                            if (current >= number) {{
                                target.textContent = text;
                                clearInterval(timer);
                            }} else {{
                                target.textContent = Math.floor(current) + text.replace(/[0-9]/g, '');
                            }}
                        }}, 50);
                    }}
                    observer.unobserve(target);
                }}
            }});
        }});

        stats.forEach(stat => observer.observe(stat));
    </script>
</body>
</html>"""

def generate_restaurant_template(prompt, title):
    """Generate a restaurant template"""
    return generate_ultra_modern_template(prompt, title)

def generate_ecommerce_template(prompt, title):
    """Generate an ecommerce template"""
    return generate_ultra_modern_template(prompt, title)

def determine_website_type(prompt):
    """Determine the type of website based on the prompt"""
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ['portfolio', 'personal', 'resume', 'cv', 'photographer', 'designer', 'artist']):
        return 'portfolio'
    elif any(word in prompt_lower for word in ['restaurant', 'food', 'menu', 'dining', 'cafe', 'bistro']):
        return 'restaurant'
    elif any(word in prompt_lower for word in ['shop', 'store', 'ecommerce', 'product', 'buy', 'sell', 'marketplace']):
        return 'ecommerce'
    elif any(word in prompt_lower for word in ['business', 'company', 'corporate', 'professional', 'startup']):
        return 'business'
    else:
        return 'general'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth')
def auth_page():
    return render_template('auth.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/generate-website', methods=['POST'])
def generate_website():
    try:
        data = request.json
        prompt = data.get('prompt', '')
        user_id = data.get('user_id', '')
        
        # For development without Firebase, allow anonymous users
        if not user_id:
            user_id = 'anonymous_user'
        
        print(f"🚀 Generating website for prompt: {prompt}")
        
        # Try multiple AI services in order of quality (all free!)
        try:
            print("🤖 Trying Gemini 1.5 Flash...")
            website_code = generate_with_gemini(prompt)
            model_used = 'gemini-1.5-flash'
            print("✅ Gemini 1.5 Flash successful!")
        except Exception as gemini_error:
            print(f"❌ Gemini API failed: {gemini_error}")
            try:
                print("🤖 Trying Groq...")
                website_code = generate_with_groq(prompt)
                model_used = 'llama3-8b-8192'
                print("✅ Groq successful!")
            except Exception as groq_error:
                print(f"❌ Groq API failed: {groq_error}")
                try:
                    print("🤖 Trying Hugging Face...")
                    website_code = generate_with_huggingface(prompt)
                    model_used = 'huggingface-codellama'
                    print("✅ Hugging Face successful!")
                except Exception as hf_error:
                    print(f"❌ Hugging Face API failed: {hf_error}")
                    print("🎨 Using premium fallback generator...")
                    website_code = generate_premium_website(prompt)
                    model_used = 'premium_template'
                    print("✅ Premium template generated!")
        
        # Save project to Firebase (or mock)
        project_id = str(uuid.uuid4())
        project_data = {
            'id': project_id,
            'user_id': user_id,
            'prompt': prompt,
            'code': website_code,
            'created_at': datetime.now().isoformat() if not FIREBASE_ENABLED else firestore.SERVER_TIMESTAMP,
            'updated_at': datetime.now().isoformat() if not FIREBASE_ENABLED else firestore.SERVER_TIMESTAMP,
            'title': extract_title_from_prompt(prompt),
            'tags': extract_tags_from_prompt(prompt),
            'is_public': False,
            'version': 1
        }
        
        try:
            if FIREBASE_ENABLED:
                db.collection('projects').document(project_id).set(project_data)
                print("💾 Project saved to Firebase")
            else:
                print("⚠️  Could not save to Firebase (using mock)")
        except Exception as e:
            print(f"⚠️  Firebase save error: {e}")
        
        # Log analytics
        try:
            if FIREBASE_ENABLED:
                analytics_data = {
                    'user_id': user_id,
                    'action': 'website_generated',
                    'timestamp': firestore.SERVER_TIMESTAMP,
                    'metadata': {
                        'prompt_length': len(prompt),
                        'model_used': model_used,
                        'project_id': project_id
                    }
                }
                db.collection('analytics').add(analytics_data)
                print("📊 Analytics logged")
            else:
                print("⚠️  Could not log analytics (using mock)")
        except Exception as e:
            print(f"⚠️  Analytics error: {e}")
        
        return jsonify({
            'success': True,
            'project_id': project_id,
            'code': website_code,
            'title': project_data['title']
        })
        
    except Exception as e:
        print(f"❌ Error generating website: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

def generate_with_gemini(prompt):
    """Generate website code using Google Gemini 1.5 Flash (Updated model name)"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    system_prompt = """You are an expert web developer and designer. Generate a complete, stunning, modern HTML website based on the user's prompt.

REQUIREMENTS:
1. Create a BREATHTAKING, modern design with beautiful gradients, glassmorphism, and animations
2. Include ALL CSS styles inline within <style> tags in the <head>
3. Include ALL JavaScript inline within <script> tags
4. Use cutting-edge CSS: flexbox, grid, CSS variables, backdrop-filter, custom properties
5. Include proper meta tags and perfect mobile responsiveness
6. Use semantic HTML5 elements
7. Add smooth animations, micro-interactions, and hover effects
8. Use a stunning color palette with gradients and modern typography
9. Include Font Awesome icons and Google Fonts (Inter, Poppins, or similar)
10. Make it look like it was designed by Apple or Google's design team
11. Add interactive elements and modern UI patterns
12. Include glassmorphism effects, floating cards, and 3D transforms
13. Add scroll animations and parallax effects
14. Return ONLY the complete HTML code, nothing else

The website should be absolutely stunning, modern, and professional - like a premium SaaS landing page with glassmorphism design."""
    
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"{system_prompt}\n\nUser request: {prompt}"}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 4000
        }
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        generated_code = result['candidates'][0]['content']['parts'][0]['text']
        
        # Clean up the response
        if '```html' in generated_code:
            generated_code = generated_code.split('```html')[1].split('```')[0].strip()
        elif '```' in generated_code:
            generated_code = generated_code.split('```')[1].strip()
        
        return generated_code
    else:
        raise Exception(f"Gemini API error: {response.status_code} - {response.text}")

def generate_with_groq(prompt):
    """Generate website code using Groq API"""
    api_key = GROQ_API_KEY
    if api_key.endswith("Firebase"):
        api_key = api_key[:-8]
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    system_prompt = """You are an expert web developer and designer. Generate a complete, modern, responsive HTML website based on the user's prompt.

Requirements:
1. Create a STUNNING, modern design with beautiful gradients, glassmorphism, and animations
2. Include ALL CSS styles inline within <style> tags in the <head>
3. Include ALL JavaScript inline within <script> tags
4. Use modern CSS features: flexbox, grid, CSS variables, backdrop-filter, gradients
5. Include proper meta tags and mobile responsiveness
6. Use semantic HTML elements
7. Add smooth animations, transitions, and hover effects
8. Use a beautiful color scheme with gradients and modern typography
9. Include Font Awesome icons and Google Fonts
10. Make it look like a premium, professional website with glassmorphism effects
11. Return ONLY the complete HTML code, nothing else

The website should look absolutely stunning and modern."""
    
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 4000,
        "temperature": 0.7
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        generated_code = result['choices'][0]['message']['content']
        
        # Clean up the response
        if '```html' in generated_code:
            generated_code = generated_code.split('```html')[1].split('```')[0].strip()
        elif '```' in generated_code:
            generated_code = generated_code.split('```')[1].strip()
        
        return generated_code
    else:
        raise Exception(f"Groq API error: {response.status_code} - {response.text}")

def generate_with_huggingface(prompt):
    """Generate website code using Hugging Face API (Free alternative)"""
    url = "https://api-inference.huggingface.co/models/codellama/CodeLlama-7b-Instruct-hf"
    
    headers = {
        "Authorization": f"Bearer {HUGGING_FACE_TOKEN}",
        "Content-Type": "application/json"
    }
    
    system_prompt = f"""Generate a complete, modern HTML website based on this prompt: {prompt}

Requirements:
- Include ALL CSS inline in <style> tags
- Include ALL JavaScript inline in <script> tags  
- Use modern design with gradients and animations
- Make it responsive and beautiful
- Include Font Awesome icons
- Return ONLY the HTML code

Generate the complete HTML:"""
    
    payload = {
        "inputs": system_prompt,
        "parameters": {
            "max_new_tokens": 2000,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            generated_code = result[0].get('generated_text', '')
            
            # Clean up the response
            if '```html' in generated_code:
                generated_code = generated_code.split('```html')[1].split('```')[0].strip()
            elif '```' in generated_code:
                generated_code = generated_code.split('```')[1].strip()
            
            return generated_code
        else:
            raise Exception("Invalid response format from Hugging Face")
    else:
        raise Exception(f"Hugging Face API error: {response.status_code} - {response.text}")

@app.route('/api/get-projects/<user_id>')
def get_user_projects(user_id):
    try:
        projects = []
        try:
            if FIREBASE_ENABLED:
                docs = db.collection('projects').where('user_id', '==', user_id).order_by('created_at', direction=firestore.Query.DESCENDING).stream()
                
                for doc in docs:
                    project = doc.to_dict()
                    if 'created_at' in project and hasattr(project['created_at'], 'timestamp'):
                        project['created_at'] = project['created_at'].timestamp()
                    if 'updated_at' in project and hasattr(project['updated_at'], 'timestamp'):
                        project['updated_at'] = project['updated_at'].timestamp()
                    projects.append(project)
            else:
                print("⚠️  Using mock projects data")
                # Return mock data for development
                projects = [
                    {
                        'id': 'sample1',
                        'title': 'Sample Portfolio',
                        'prompt': 'Create a modern portfolio website',
                        'created_at': datetime.now().timestamp(),
                        'tags': ['portfolio', 'modern']
                    }
                ]
        except Exception as e:
            print(f"⚠️  Firebase query error: {e}")
            projects = []
            
        return jsonify({'success': True, 'projects': projects})
        
    except Exception as e:
        print(f"❌ Error getting projects: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/download-project/<project_id>')
def download_project(project_id):
    try:
        try:
            if FIREBASE_ENABLED:
                doc = db.collection('projects').document(project_id).get()
                if doc.exists:
                    project = doc.to_dict()
                else:
                    return jsonify({'error': 'Project not found'}), 404
            else:
                # Mock project for development
                project = {
                    'title': 'Sample Website',
                    'code': generate_premium_website('Sample website for download')
                }
        except Exception as e:
            print(f"⚠️  Firebase download error: {e}")
            project = {
                'title': 'Sample Website',
                'code': generate_premium_website('Sample website for download')
            }
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8')
        temp_file.write(project['code'])
        temp_file.close()
        
        filename = f"{project.get('title', 'website').replace(' ', '_')}.html"
        
        return send_file(temp_file.name, as_attachment=True, 
                       download_name=filename, mimetype='text/html')
        
    except Exception as e:
        print(f"❌ Error downloading project: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/delete-project/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    try:
        try:
            if FIREBASE_ENABLED:
                doc = db.collection('projects').document(project_id).get()
                if not doc.exists:
                    return jsonify({'error': 'Project not found'}), 404
                
                db.collection('projects').document(project_id).delete()
            else:
                print("⚠️  Mock delete operation")
        except Exception as e:
            print(f"⚠️  Firebase delete error: {e}")
        
        return jsonify({'success': True, 'message': 'Project deleted successfully'})
        
    except Exception as e:
        print(f"❌ Error deleting project: {str(e)}")
        return jsonify({'error': str(e)}), 500

def extract_title_from_prompt(prompt):
    """Extract a title from the prompt"""
    stop_words = {'create', 'make', 'build', 'design', 'a', 'an', 'the', 'for', 'with', 'website', 'page', 'site'}
    words = [word.capitalize() for word in prompt.split() if word.lower() not in stop_words]
    title = ' '.join(words[:4]) if words else 'My Website'
    return title

def extract_tags_from_prompt(prompt):
    """Extract relevant tags from the prompt"""
    common_tags = {
        'portfolio': ['portfolio', 'personal', 'resume', 'cv'],
        'business': ['business', 'company', 'corporate', 'professional'],
        'ecommerce': ['shop', 'store', 'ecommerce', 'product', 'buy', 'sell'],
        'blog': ['blog', 'article', 'news', 'content'],
        'landing': ['landing', 'marketing', 'promotion', 'campaign'],
        'restaurant': ['restaurant', 'food', 'menu', 'dining'],
        'photography': ['photography', 'photographer', 'gallery', 'photos'],
        'tech': ['tech', 'technology', 'software', 'app', 'startup'],
        'creative': ['creative', 'art', 'design', 'artist'],
        'education': ['education', 'school', 'course', 'learning']
    }
    
    tags = []
    prompt_lower = prompt.lower()
    
    for tag, keywords in common_tags.items():
        if any(keyword in prompt_lower for keyword in keywords):
            tags.append(tag)
    
    return tags[:3]

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print("🚀 Starting AI Website Builder...")
    print("📋 Setup Instructions:")
    print("1. Add firebase-credentials.json to your project folder")
    print("2. Or continue with mock Firebase for development")
    print("3. Your Gemini API key is configured ✅")
    print("4. Visit http://localhost:5000 to start building!")
    print("\n🎯 Ready to generate stunning websites!")
    app.run(debug=True, host='0.0.0.0', port=5000)
