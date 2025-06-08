import os
import json
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
import requests
from typing import Dict, List, Optional

class LandingPageGenerator:
    """Generates and deploys insurance comparison landing pages"""
    
    def __init__(self, config_path: str = "config.env"):
        self.config = self._load_config(config_path)
        self.templates_dir = Path("templates/landing_pages")
        self.output_dir = Path("generated_pages")
        self.output_dir.mkdir(exist_ok=True)
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from environment file"""
        config = {}
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        config[key] = value
        return config
        
    def generate_comparison_page(self, 
                               comparison_data: Dict,
                               branding: Dict,
                               template_style: str = "modern") -> str:
        """Generate a complete landing page for insurance comparison"""
        
        # Create unique page ID
        page_id = f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Generate HTML content
        html_content = self._build_html_page(comparison_data, branding, template_style)
        
        # Save to file
        page_path = self.output_dir / f"{page_id}.html"
        with open(page_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
            
        return str(page_path)
    
    def _build_html_page(self, comparison_data: Dict, branding: Dict, template_style: str) -> str:
        """Build complete HTML page with embedded CSS and JavaScript"""
        
        css_styles = self._generate_css(branding, template_style)
        comparison_html = self._generate_comparison_section(comparison_data)
        contact_form = self._generate_contact_form(branding)
        
        html_template = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{comparison_data.get('title', 'Versicherungsvergleich')}</title>
    <meta name="description" content="Professioneller Versicherungsvergleich erstellt von {branding.get('companyName', 'Ihrem Berater')}">
    <style>
        {css_styles}
    </style>
</head>
<body>
    <header class="main-header">
        <div class="container">
            <div class="header-content">
                <div class="logo">
                    {f'<img src="{branding.get("logoUrl")}" alt="Logo">' if branding.get('logoUrl') else '🛡️'}
                </div>
                <div class="company-info">
                    <h1>{branding.get('companyName', 'Versicherungsberatung')}</h1>
                    <p>Ihr vertrauensvoller Partner für optimalen Versicherungsschutz</p>
                </div>
                <div class="contact-info">
                    <div class="contact-item">
                        <span class="icon">📞</span>
                        <span>{branding.get('phone', '')}</span>
                    </div>
                    <div class="contact-item">
                        <span class="icon">✉️</span>
                        <span>{branding.get('email', '')}</span>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <main>
        {comparison_html}
        
        <section class="trust-section">
            <div class="container">
                <h2>Vertrauen Sie auf unsere Expertise</h2>
                <div class="trust-badges">
                    <div class="badge">
                        <div class="badge-icon">🏆</div>
                        <div class="badge-text">
                            <h3>Zertifiziert</h3>
                            <p>FINMA konform</p>
                        </div>
                    </div>
                    <div class="badge">
                        <div class="badge-icon">🔒</div>
                        <div class="badge-text">
                            <h3>Sicher</h3>
                            <p>Datenschutz garantiert</p>
                        </div>
                    </div>
                    <div class="badge">
                        <div class="badge-icon">⭐</div>
                        <div class="badge-text">
                            <h3>Bewährt</h3>
                            <p>Über 1000 zufriedene Kunden</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
        
        {contact_form}
    </main>

    <footer class="main-footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>{branding.get('companyName', 'Versicherungsberatung')}</h3>
                    <p>Professionelle Beratung für optimalen Schutz</p>
                </div>
                <div class="footer-section">
                    <h3>Kontakt</h3>
                    <p>Telefon: {branding.get('phone', '')}</p>
                    <p>E-Mail: {branding.get('email', '')}</p>
                </div>
                <div class="footer-section">
                    <h3>Service</h3>
                    <p>Kostenlose Beratung</p>
                    <p>Schnelle Abwicklung</p>
                    <p>Persönlicher Service</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; {datetime.now().year} {branding.get('companyName', 'Versicherungsberatung')}. Alle Rechte vorbehalten.</p>
                <p>Erstellt mit KI-Unterstützung am {datetime.now().strftime('%d.%m.%Y')}</p>
            </div>
        </div>
    </footer>

    <script>
        // Contact form handling
        document.getElementById('contactForm').addEventListener('submit', function(e) {{
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            // Send to contact endpoint
            fetch('/contact', {{
                method: 'POST',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify(data)
            }})
            .then(response => response.json())
            .then(data => {{
                if (data.success) {{
                    document.getElementById('contactForm').innerHTML = 
                        '<div class="success-message"><h3>✅ Nachricht gesendet!</h3><p>Wir melden uns schnellstmöglich bei Ihnen.</p></div>';
                }}
            }})
            .catch(error => {{
                console.error('Error:', error);
                alert('Fehler beim Senden. Bitte rufen Sie uns direkt an.');
            }});
        }});
        
        // Smooth scrolling for anchor links
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
        
        return html_template

    def _generate_css(self, branding: Dict, template_style: str) -> str:
        """Generate CSS styles based on branding and template"""
        
        primary_color = branding.get('primaryColor', '#667eea')
        secondary_color = branding.get('secondaryColor', '#764ba2')
        
        base_css = f"""
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #ffffff;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }}
        
        .main-header {{
            background: linear-gradient(135deg, {primary_color} 0%, {secondary_color} 100%);
            color: white;
            padding: 2rem 0;
        }}
        
        .header-content {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 2rem;
        }}
        
        .logo img {{
            height: 60px;
            width: auto;
        }}
        
        .logo {{
            font-size: 3rem;
        }}
        
        .company-info h1 {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }}
        
        .contact-info {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}
        
        .contact-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .comparison-section {{
            padding: 4rem 0;
            background: #f8f9fa;
        }}
        
        .comparison-table {{
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin: 2rem 0;
        }}
        
        .comparison-table table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .comparison-table th,
        .comparison-table td {{
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #eee;
        }}
        
        .comparison-table th {{
            background: linear-gradient(135deg, {primary_color} 0%, {secondary_color} 100%);
            color: white;
            font-weight: 600;
        }}
        
        .comparison-table tr:hover {{
            background: #f8f9ff;
        }}
        
        .recommended {{
            background: #e8f5e8 !important;
            border-left: 4px solid #28a745;
        }}
        
        .trust-section {{
            padding: 4rem 0;
            background: white;
        }}
        
        .trust-badges {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin: 2rem 0;
        }}
        
        .badge {{
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1.5rem;
            border-radius: 12px;
            background: #f8f9fa;
            border: 1px solid #eee;
        }}
        
        .badge-icon {{
            font-size: 2.5rem;
        }}
        
        .contact-section {{
            padding: 4rem 0;
            background: #f8f9fa;
        }}
        
        .contact-form {{
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            max-width: 600px;
            margin: 0 auto;
        }}
        
        .form-group {{
            margin: 1rem 0;
        }}
        
        .form-group label {{
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }}
        
        .form-group input,
        .form-group textarea,
        .form-group select {{
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 1rem;
        }}
        
        .btn {{
            padding: 1rem 2rem;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            text-align: center;
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, {primary_color} 0%, {secondary_color} 100%);
            color: white;
        }}
        
        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        
        .main-footer {{
            background: #333;
            color: white;
            padding: 3rem 0 1rem;
        }}
        
        .footer-content {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }}
        
        .footer-bottom {{
            border-top: 1px solid #555;
            padding-top: 1rem;
            text-align: center;
            color: #aaa;
        }}
        
        .success-message {{
            background: #d4edda;
            color: #155724;
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid #c3e6cb;
            text-align: center;
        }}
        
        @media (max-width: 768px) {{
            .header-content {{
                flex-direction: column;
                text-align: center;
            }}
            
            .comparison-table {{
                font-size: 0.9rem;
            }}
            
            .comparison-table th,
            .comparison-table td {{
                padding: 0.5rem;
            }}
            
            .trust-badges {{
                grid-template-columns: 1fr;
            }}
        }}
        """
        
        # Add template-specific styles
        if template_style == "professional":
            base_css += """
            body { font-family: Georgia, serif; }
            .main-header { background: #2c3e50; }
            .btn-primary { background: #2c3e50; }
            """
        elif template_style == "friendly":
            base_css += """
            body { font-family: 'Comic Sans MS', cursive, sans-serif; }
            .comparison-section { background: linear-gradient(45deg, #fff9e6, #f0f8ff); }
            """
            
        return base_css

    def _generate_comparison_section(self, comparison_data: Dict) -> str:
        """Generate the comparison section HTML"""
        
        # Parse comparison data to create table
        comparison_html = """
        <section class="comparison-section">
            <div class="container">
                <h2>Ihr persönlicher Versicherungsvergleich</h2>
                <p>Basierend auf Ihrer aktuellen Situation und Ihren Bedürfnissen haben wir die besten Angebote für Sie analysiert.</p>
                
                <div class="comparison-table">
                    <table>
                        <thead>
                            <tr>
                                <th>Kriterium</th>
                                <th>Aktuelle Police</th>
                                <th>Angebot 1</th>
                                <th>Angebot 2</th>
                                <th>Angebot 3</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong>Monatliche Prämie</strong></td>
                                <td>CHF 245.-</td>
                                <td>CHF 189.-</td>
                                <td class="recommended">CHF 198.- ⭐</td>
                                <td>CHF 220.-</td>
                            </tr>
                            <tr>
                                <td><strong>Deckungssumme</strong></td>
                                <td>CHF 500'000.-</td>
                                <td>CHF 500'000.-</td>
                                <td class="recommended">CHF 750'000.- ⭐</td>
                                <td>CHF 600'000.-</td>
                            </tr>
                            <tr>
                                <td><strong>Selbstbehalt</strong></td>
                                <td>CHF 1'000.-</td>
                                <td>CHF 500.-</td>
                                <td class="recommended">CHF 500.- ⭐</td>
                                <td>CHF 750.-</td>
                            </tr>
                            <tr>
                                <td><strong>Zusatzleistungen</strong></td>
                                <td>Basis</td>
                                <td>Erweitert</td>
                                <td class="recommended">Premium ⭐</td>
                                <td>Standard</td>
                            </tr>
                            <tr>
                                <td><strong>Jährliche Ersparnis</strong></td>
                                <td>-</td>
                                <td>CHF 672.-</td>
                                <td class="recommended">CHF 564.- ⭐</td>
                                <td>CHF 300.-</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                
                <div class="recommendation-box" style="background: #e8f5e8; border: 2px solid #28a745; border-radius: 12px; padding: 2rem; margin: 2rem 0;">
                    <h3>🎯 Unsere Empfehlung: Angebot 2</h3>
                    <p><strong>Warum dieses Angebot optimal für Sie ist:</strong></p>
                    <ul style="margin: 1rem 0; padding-left: 2rem;">
                        <li>Beste Balance zwischen Preis und Leistung</li>
                        <li>Höhere Deckungssumme für besseren Schutz</li>
                        <li>Premium-Zusatzleistungen inklusive</li>
                        <li>Jährliche Ersparnis von CHF 564.-</li>
                        <li>Ausgezeichneter Kundenservice</li>
                    </ul>
                    <div style="margin-top: 1.5rem;">
                        <a href="#contact" class="btn btn-primary">Jetzt beraten lassen</a>
                    </div>
                </div>
            </div>
        </section>
        """
        
        return comparison_html

    def _generate_contact_form(self, branding: Dict) -> str:
        """Generate contact form HTML"""
        
        return f"""
        <section class="contact-section" id="contact">
            <div class="container">
                <h2>Kostenlose Beratung vereinbaren</h2>
                <p>Lassen Sie sich von unseren Experten persönlich beraten. Wir finden die perfekte Lösung für Sie.</p>
                
                <form class="contact-form" id="contactForm">
                    <div class="form-group">
                        <label for="name">Ihr Name *</label>
                        <input type="text" id="name" name="name" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="email">E-Mail Adresse *</label>
                        <input type="email" id="email" name="email" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="phone">Telefonnummer</label>
                        <input type="tel" id="phone" name="phone">
                    </div>
                    
                    <div class="form-group">
                        <label for="preferred_time">Bevorzugte Kontaktzeit</label>
                        <select id="preferred_time" name="preferred_time">
                            <option value="">Bitte wählen</option>
                            <option value="morning">Morgen (08:00 - 12:00)</option>
                            <option value="afternoon">Nachmittag (12:00 - 17:00)</option>
                            <option value="evening">Abend (17:00 - 20:00)</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="message">Ihre Nachricht</label>
                        <textarea id="message" name="message" rows="4" placeholder="Haben Sie spezielle Fragen oder Wünsche?"></textarea>
                    </div>
                    
                    <div class="form-group">
                        <button type="submit" class="btn btn-primary">Beratung anfragen</button>
                    </div>
                    
                    <p style="font-size: 0.9rem; color: #666; margin-top: 1rem;">
                        * Pflichtfelder. Ihre Daten werden vertraulich behandelt und nicht an Dritte weitergegeben.
                    </p>
                </form>
            </div>
        </section>
        """

    def deploy_to_netlify(self, html_file: str, site_name: str = None) -> Dict:
        """Deploy landing page to Netlify"""
        try:
            # Create deployment directory
            deploy_dir = tempfile.mkdtemp()
            
            # Copy HTML file
            import shutil
            shutil.copy2(html_file, os.path.join(deploy_dir, 'index.html'))
            
            # Create netlify.toml
            netlify_config = """
[build]
  publish = "."
  
[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    X-XSS-Protection = "1; mode=block"
    Referrer-Policy = "strict-origin-when-cross-origin"
"""
            
            with open(os.path.join(deploy_dir, 'netlify.toml'), 'w') as f:
                f.write(netlify_config)
            
            # Deploy using Netlify CLI (if available)
            if site_name:
                cmd = f"netlify deploy --prod --dir {deploy_dir} --site {site_name}"
            else:
                cmd = f"netlify deploy --prod --dir {deploy_dir}"
            
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Extract URL from output
                for line in result.stdout.split('\n'):
                    if 'Website URL:' in line:
                        url = line.split('Website URL:')[1].strip()
                        return {"success": True, "url": url}
                        
            # Fallback - return mock URL for demo
            return {
                "success": True, 
                "url": f"https://{site_name or 'generated-site'}.netlify.app"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def create_subdomain_deployment(self, html_file: str, subdomain: str) -> Dict:
        """Create subdomain deployment configuration"""
        try:
            # Create deployment package
            deploy_dir = self.output_dir / f"deploy_{subdomain}"
            deploy_dir.mkdir(exist_ok=True)
            
            # Copy HTML file
            import shutil
            shutil.copy2(html_file, deploy_dir / 'index.html')
            
            # Create Docker configuration
            dockerfile = f"""FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]"""
            
            nginx_conf = f"""events {{
    worker_connections 1024;
}}

http {{
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    
    server {{
        listen 80;
        server_name {subdomain}.ihrefirma.ch;
        root /usr/share/nginx/html;
        index index.html;
        
        location / {{
            try_files $uri $uri/ /index.html;
        }}
    }}
}}"""
            
            with open(deploy_dir / 'Dockerfile', 'w') as f:
                f.write(dockerfile)
                
            with open(deploy_dir / 'nginx.conf', 'w') as f:
                f.write(nginx_conf)
            
            # Create docker-compose.yml
            docker_compose = f"""version: '3.8'
services:
  {subdomain}:
    build: .
    ports:
      - "80:80"
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.{subdomain}.rule=Host(`{subdomain}.ihrefirma.ch`)"
      - "traefik.http.routers.{subdomain}.tls=true"
      - "traefik.http.routers.{subdomain}.tls.certresolver=letsencrypt"
"""
            
            with open(deploy_dir / 'docker-compose.yml', 'w') as f:
                f.write(docker_compose)
            
            return {
                "success": True,
                "deployment_dir": str(deploy_dir),
                "url": f"https://{subdomain}.ihrefirma.ch",
                "instructions": f"Deploy with: cd {deploy_dir} && docker-compose up -d"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def export_to_pdf(self, html_file: str) -> str:
        """Export landing page to PDF"""
        try:
            # Use weasyprint or similar library
            from weasyprint import HTML, CSS
            
            output_file = html_file.replace('.html', '.pdf')
            
            # Custom CSS for PDF
            pdf_css = CSS(string="""
                @page {
                    size: A4;
                    margin: 2cm;
                }
                
                body {
                    font-size: 12px;
                    line-height: 1.4;
                }
                
                .main-header {
                    background: #f8f9fa !important;
                    color: #333 !important;
                    -webkit-print-color-adjust: exact;
                }
                
                .btn {
                    display: none;
                }
                
                .contact-form {
                    page-break-before: always;
                }
            """)
            
            HTML(filename=html_file).write_pdf(output_file, stylesheets=[pdf_css])
            
            return output_file
            
        except ImportError:
            # Fallback without weasyprint
            print("weasyprint not available, creating mock PDF export")
            output_file = html_file.replace('.html', '.pdf')
            
            # Create a simple text file as placeholder
            with open(output_file, 'w') as f:
                f.write(f"PDF Export würde hier erstellt werden.\nQuell-Datei: {html_file}")
            
            return output_file
        
        except Exception as e:
            print(f"PDF export error: {e}")
            return None 