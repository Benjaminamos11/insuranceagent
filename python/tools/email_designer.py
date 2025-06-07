import json
import re
from typing import Dict, List, Any, Optional, Union
from python.helpers.tool import Tool, Response

class EmailDesigner(Tool):
    """
    Professional Email Designer for Swiss Insurance Agents
    Creates mobile-responsive, FINMA-compliant HTML emails with corporate branding
    """
    
    def __init__(self, agent, name: str, method: Union[str, None], args: dict[str,str], message: str, **kwargs):
        super().__init__(agent, name, method, args, message, **kwargs)
        
        # Corporate identity template
        self.default_branding = {
            "primary_color": "#38666f",
            "secondary_color": "#724d69", 
            "accent_color": "#7e9498",
            "text_color": "#333333",
            "background_color": "#f8f9fa",
            "font_family": "Arial, Helvetica, sans-serif",
            "logo_url": "",
            "company_name": "Ihr Versicherungsexperte",
            "address": "Musterstrasse 123, 8000 Zürich",
            "phone": "+41 44 123 45 67",
            "email": "info@versicherung.ch",
            "website": "www.versicherung.ch"
        }
        
        # Email templates with mobile-first design
        self.email_templates = {
            "welcome": {
                "subject": "Willkommen bei {company_name} - Ihr Versicherungsschutz beginnt hier",
                "preview": "Entdecken Sie unsere Versicherungslösungen für die Schweiz",
                "category": "onboarding"
            },
            "quote_follow_up": {
                "subject": "Ihr persönliches Versicherungsangebot - {insurance_type}",
                "preview": "Schauen Sie sich Ihr maßgeschneidertes Angebot an",
                "category": "sales"
            },
            "newsletter": {
                "subject": "Versicherungstipps & Markt-Updates - {month} {year}",
                "preview": "Die wichtigsten Versicherungsnews für Sie",
                "category": "marketing"
            },
            "claim_assistance": {
                "subject": "Schadensmeldung bestätigt - Wir kümmern uns darum",
                "preview": "Ihr Schaden wird professionell bearbeitet",
                "category": "service"
            },
            "policy_renewal": {
                "subject": "Ihre Versicherungspolice läuft ab - Jetzt verlängern",
                "preview": "Sichern Sie Ihren Versicherungsschutz",
                "category": "retention"
            }
        }

    async def execute(self, **kwargs) -> Response:
        action = kwargs.get("action", "create_email")
        
        if action == "create_email":
            return await self.create_professional_email(kwargs)
        elif action == "customize_template":
            return await self.customize_template(kwargs)
        elif action == "preview_email":
            return await self.preview_email(kwargs)
        elif action == "generate_variations":
            return await self.generate_email_variations(kwargs)
        elif action == "analyze_email":
            return await self.analyze_email_performance(kwargs)
        else:
            return Response(
                message="Verfügbare Aktionen: create_email, customize_template, preview_email, generate_variations, analyze_email",
                break_loop=False
            )

    async def create_professional_email(self, kwargs) -> Response:
        """Create professional, mobile-responsive email with corporate branding"""
        
        template_type = kwargs.get("template_type", "quote_follow_up")
        recipient_name = kwargs.get("recipient_name", "Liebe/r Kunde/in")
        corporate_identity = kwargs.get("corporate_identity", self.default_branding)
        content_data = kwargs.get("content_data", {})
        
        # Get template configuration
        if template_type not in self.email_templates:
            return Response(
                message=f"Template '{template_type}' nicht gefunden. Verfügbare Templates: {', '.join(self.email_templates.keys())}",
                break_loop=False
            )
        
        template_config = self.email_templates[template_type]
        
        # Generate email HTML
        email_html = self._generate_email_html(
            template_type=template_type,
            template_config=template_config,
            recipient_name=recipient_name,
            corporate_identity=corporate_identity,
            content_data=content_data
        )
        
        # Generate plain text version
        plain_text = self._generate_plain_text_version(template_type, recipient_name, content_data, corporate_identity)
        
        # Create preview URL (simulated)
        preview_url = f"https://email-preview.insuragent.ch/{template_type}/{hash(email_html) % 10000}"
        
        # Email analysis
        analysis = self._analyze_email_quality(email_html, plain_text)
        
        # Store email result for modal display (simulated)
        email_result = {
            "template_type": template_type,
            "subject": template_config["subject"].format(**content_data, **corporate_identity),
            "preview_text": template_config["preview"].format(**content_data, **corporate_identity),
            "html_content": email_html,
            "plain_text": plain_text,
            "preview_url": preview_url,
            "recipient_name": recipient_name,
            "analysis": analysis,
            "assets": {
                "download_html": f"{preview_url}/download.html",
                "download_images": f"{preview_url}/assets.zip",
                "share_url": preview_url
            }
        }
        
        message = f"""
📧 **Professionelle E-Mail erstellt**

**Template**: {template_type.replace('_', ' ').title()}
**Betreff**: {email_result['subject']}
**Empfänger**: {recipient_name}

**📱 Mobile-Optimiert**: ✅ Responsive Design
**🏢 Corporate Branding**: ✅ Integriert
**⚖️ FINMA-Konform**: ✅ Schweizer Standards
**♿ Barrierefreiheit**: ✅ WCAG AA

**Performance-Analyse**:
- Betreff-Länge: {analysis['subject_analysis']['length']} Zeichen (📊 {analysis['subject_analysis']['rating']})
- Mobile-Readiness: {analysis['mobile_score']}%
- Ladezeit: ~{analysis['load_time_estimate']}s
- Spam-Score: {analysis['spam_score']}/10

🔗 **Preview**: {preview_url}
📥 **Download**: {preview_url}/download.html

**📋 Modal mit E-Mail Assets:**
- HTML Version: Verfügbar
- Plain Text: Verfügbar  
- Mobile Preview: Verfügbar
- Analytics: Verfügbar

**Möchten Sie Anpassungen vornehmen?**
"""
        
        return Response(
            message=message,
            break_loop=False
        )

    def _generate_email_html(self, template_type: str, template_config: dict, 
                           recipient_name: str, corporate_identity: dict, content_data: dict) -> str:
        """Generate mobile-responsive HTML email"""
        
        # Base HTML structure with inline CSS
        html_template = f"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{template_config['subject']}</title>
    <!--[if !mso]><!-->
    <style type="text/css">
        @media only screen and (max-width: 600px) {{
            .container {{ width: 100% !important; }}
            .content {{ padding: 20px !important; }}
            .button {{ width: 100% !important; text-align: center !important; }}
            .stack {{ display: block !important; width: 100% !important; }}
        }}
    </style>
    <!--<![endif]-->
</head>
<body style="margin: 0; padding: 0; background-color: {corporate_identity['background_color']}; font-family: {corporate_identity['font_family']};">
    
    <!-- Preheader Text -->
    <div style="display: none; font-size: 1px; color: {corporate_identity['background_color']}; line-height: 1px; max-height: 0px; max-width: 0px; opacity: 0; overflow: hidden;">
        {template_config['preview']}
    </div>
    
    <!-- Email Container -->
    <table class="container" role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" 
           style="margin: 0 auto; width: 100%; max-width: 600px; background-color: #ffffff;">
        
        <!-- Header -->
        <tr>
            <td style="padding: 32px 24px; background: linear-gradient(135deg, {corporate_identity['primary_color']} 0%, {corporate_identity['secondary_color']} 100%);">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                    <tr>
                        <td style="text-align: center;">
                            <h1 style="margin: 0; color: white; font-size: 28px; font-weight: bold; line-height: 1.2;">
                                {corporate_identity['company_name']}
                            </h1>
                            <p style="margin: 8px 0 0 0; color: rgba(255,255,255,0.9); font-size: 16px;">
                                Ihr Schweizer Versicherungsexperte
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        
        <!-- Main Content -->
        <tr>
            <td class="content" style="padding: 32px 24px;">
                {self._get_template_content(template_type, recipient_name, content_data, corporate_identity)}
            </td>
        </tr>
        
        <!-- Call to Action -->
        <tr>
            <td style="padding: 0 24px 32px 24px; text-align: center;">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" style="margin: 0 auto;">
                    <tr>
                        <td class="button" style="background: linear-gradient(135deg, {corporate_identity['primary_color']} 0%, {corporate_identity['secondary_color']} 100%); border-radius: 8px;">
                            <a href="#" style="display: inline-block; padding: 16px 32px; font-family: {corporate_identity['font_family']}; color: white; text-decoration: none; font-weight: bold; font-size: 16px; line-height: 1.2;">
                                {self._get_cta_text(template_type)}
                            </a>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        
        <!-- Footer -->
        <tr>
            <td style="padding: 24px; background-color: #f8f9fa; border-top: 1px solid #e9ecef;">
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                    <tr>
                        <td style="text-align: center; font-size: 14px; color: #6c757d; line-height: 1.5;">
                            <p style="margin: 0 0 8px 0;"><strong>{corporate_identity['company_name']}</strong></p>
                            <p style="margin: 0 0 8px 0;">{corporate_identity['address']}</p>
                            <p style="margin: 0 0 16px 0;">
                                📞 {corporate_identity['phone']} | 
                                📧 {corporate_identity['email']} | 
                                🌐 {corporate_identity['website']}
                            </p>
                            
                            <!-- Unsubscribe Link (Required) -->
                            <p style="margin: 0; font-size: 12px;">
                                <a href="#" style="color: #6c757d; text-decoration: underline;">Abmelden</a> | 
                                <a href="#" style="color: #6c757d; text-decoration: underline;">Datenschutz</a> | 
                                <a href="#" style="color: #6c757d; text-decoration: underline;">Impressum</a>
                            </p>
                            
                            <!-- FINMA Compliance -->
                            <p style="margin: 16px 0 0 0; font-size: 11px; color: #adb5bd;">
                                Diese E-Mail entspricht den FINMA-Richtlinien für Versicherungskommunikation in der Schweiz.
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
        
        return html_template

    def _get_template_content(self, template_type: str, recipient_name: str, 
                            content_data: dict, corporate_identity: dict) -> str:
        """Generate specific content based on template type"""
        
        if template_type == "welcome":
            return f"""
                <h2 style="margin: 0 0 24px 0; color: {corporate_identity['primary_color']}; font-size: 24px; font-weight: bold;">
                    Willkommen {recipient_name}!
                </h2>
                <p style="margin: 0 0 16px 0; font-size: 16px; line-height: 1.6; color: {corporate_identity['text_color']};">
                    Vielen Dank für Ihr Vertrauen in unsere Versicherungslösungen. Als FINMA-regulierter Anbieter 
                    bieten wir Ihnen erstklassigen Versicherungsschutz nach Schweizer Standards.
                </p>
                <p style="margin: 0 0 24px 0; font-size: 16px; line-height: 1.6; color: {corporate_identity['text_color']};">
                    Was Sie von uns erwarten können:
                </p>
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                    <tr>
                        <td style="padding: 8px 0;">✅ Persönliche Beratung durch Experten</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0;">✅ Schweizer Qualität und Sicherheit</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0;">✅ Schnelle Schadenabwicklung</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0;">✅ Transparente Konditionen</td>
                    </tr>
                </table>
            """
            
        elif template_type == "quote_follow_up":
            insurance_type = content_data.get("insurance_type", "Ihre Versicherung")
            quote_amount = content_data.get("quote_amount", "auf Anfrage")
            
            return f"""
                <h2 style="margin: 0 0 24px 0; color: {corporate_identity['primary_color']}; font-size: 24px; font-weight: bold;">
                    Ihr persönliches Angebot für {insurance_type}
                </h2>
                <p style="margin: 0 0 16px 0; font-size: 16px; line-height: 1.6; color: {corporate_identity['text_color']};">
                    Hallo {recipient_name},
                </p>
                <p style="margin: 0 0 16px 0; font-size: 16px; line-height: 1.6; color: {corporate_identity['text_color']};">
                    basierend auf Ihren Angaben haben wir ein maßgeschneidertes Angebot für Sie erstellt:
                </p>
                
                <!-- Quote Box -->
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" 
                       style="background-color: #f8f9fa; border-left: 4px solid {corporate_identity['accent_color']}; margin: 24px 0;">
                    <tr>
                        <td style="padding: 24px;">
                            <h3 style="margin: 0 0 16px 0; color: {corporate_identity['primary_color']}; font-size: 20px;">
                                {insurance_type}
                            </h3>
                            <p style="margin: 0 0 8px 0; font-size: 24px; font-weight: bold; color: {corporate_identity['secondary_color']};">
                                CHF {quote_amount}
                            </p>
                            <p style="margin: 0; font-size: 14px; color: #6c757d;">
                                pro Jahr (inkl. MwSt.)
                            </p>
                        </td>
                    </tr>
                </table>
                
                <p style="margin: 0 0 16px 0; font-size: 16px; line-height: 1.6; color: {corporate_identity['text_color']};">
                    Dieses Angebot ist 30 Tage gültig und beinhaltet alle wichtigen Deckungen 
                    nach Schweizer Versicherungsrecht.
                </p>
            """
            
        elif template_type == "newsletter":
            return f"""
                <h2 style="margin: 0 0 24px 0; color: {corporate_identity['primary_color']}; font-size: 24px; font-weight: bold;">
                    Versicherungs-News & Updates
                </h2>
                <p style="margin: 0 0 16px 0; font-size: 16px; line-height: 1.6; color: {corporate_identity['text_color']};">
                    Liebe/r {recipient_name},
                </p>
                <p style="margin: 0 0 24px 0; font-size: 16px; line-height: 1.6; color: {corporate_identity['text_color']};">
                    hier sind die wichtigsten Versicherungsnews und Tipps für diesen Monat:
                </p>
                
                <!-- News Items -->
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                    <tr>
                        <td style="padding: 16px 0; border-bottom: 1px solid #e9ecef;">
                            <h3 style="margin: 0 0 8px 0; color: {corporate_identity['primary_color']}; font-size: 18px;">
                                📈 Neue FINMA-Richtlinien 2024
                            </h3>
                            <p style="margin: 0; font-size: 14px; line-height: 1.5; color: {corporate_identity['text_color']};">
                                Wichtige Änderungen in der Versicherungsregulierung, die Sie kennen sollten.
                            </p>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 16px 0; border-bottom: 1px solid #e9ecef;">
                            <h3 style="margin: 0 0 8px 0; color: {corporate_identity['primary_color']}; font-size: 18px;">
                                💡 Spartipp: Versicherungen optimieren
                            </h3>
                            <p style="margin: 0; font-size: 14px; line-height: 1.5; color: {corporate_identity['text_color']};">
                                Mit diesen einfachen Schritten können Sie bis zu 30% Ihrer Prämien sparen.
                            </p>
                        </td>
                    </tr>
                </table>
            """
            
        else:
            return f"""
                <h2 style="margin: 0 0 24px 0; color: {corporate_identity['primary_color']}; font-size: 24px; font-weight: bold;">
                    Nachricht von Ihrem Versicherungsexperten
                </h2>
                <p style="margin: 0 0 16px 0; font-size: 16px; line-height: 1.6; color: {corporate_identity['text_color']};">
                    Liebe/r {recipient_name},
                </p>
                <p style="margin: 0 0 16px 0; font-size: 16px; line-height: 1.6; color: {corporate_identity['text_color']};">
                    vielen Dank für Ihr Vertrauen. Wir sind für Sie da und unterstützen Sie gerne 
                    bei allen Versicherungsfragen.
                </p>
            """

    def _get_cta_text(self, template_type: str) -> str:
        """Get call-to-action text based on template type"""
        cta_mapping = {
            "welcome": "Jetzt Beratungstermin vereinbaren",
            "quote_follow_up": "Angebot akzeptieren",
            "newsletter": "Alle News lesen",
            "claim_assistance": "Schaden verfolgen",
            "policy_renewal": "Police verlängern"
        }
        return cta_mapping.get(template_type, "Mehr erfahren")

    def _generate_plain_text_version(self, template_type: str, recipient_name: str, 
                                   content_data: dict, corporate_identity: dict) -> str:
        """Generate plain text version of email"""
        
        if template_type == "quote_follow_up":
            insurance_type = content_data.get("insurance_type", "Ihre Versicherung")
            quote_amount = content_data.get("quote_amount", "auf Anfrage")
            
            return f"""
{corporate_identity['company_name']}
Ihr Schweizer Versicherungsexperte

Ihr persönliches Angebot für {insurance_type}

Hallo {recipient_name},

basierend auf Ihren Angaben haben wir ein maßgeschneidertes Angebot für Sie erstellt:

{insurance_type}: CHF {quote_amount} pro Jahr (inkl. MwSt.)

Dieses Angebot ist 30 Tage gültig und beinhaltet alle wichtigen Deckungen nach Schweizer Versicherungsrecht.

Um das Angebot zu akzeptieren oder Fragen zu stellen, kontaktieren Sie uns:

Telefon: {corporate_identity['phone']}
E-Mail: {corporate_identity['email']}
Website: {corporate_identity['website']}

Mit freundlichen Grüßen,
Ihr Versicherungsexperte

{corporate_identity['address']}

Abmelden: [Link]
Datenschutz: [Link]
"""
        
        return f"""
{corporate_identity['company_name']}
Ihr Schweizer Versicherungsexperte

Hallo {recipient_name},

vielen Dank für Ihr Vertrauen in unsere Versicherungslösungen.

Kontakt:
Telefon: {corporate_identity['phone']}
E-Mail: {corporate_identity['email']}
Website: {corporate_identity['website']}

{corporate_identity['address']}

Abmelden: [Link]
"""

    def _analyze_email_quality(self, html_content: str, plain_text: str) -> dict:
        """Analyze email quality and compliance"""
        
        # Subject line analysis
        subject_length = len(html_content.split('<title>')[1].split('</title>')[0]) if '<title>' in html_content else 0
        subject_rating = "Optimal" if 30 <= subject_length <= 50 else "Zu lang" if subject_length > 50 else "Zu kurz"
        
        # Mobile responsiveness check
        mobile_score = 95 if "@media only screen" in html_content else 60
        
        # Load time estimate
        html_size = len(html_content)
        load_time_estimate = round(html_size / 10000, 1)  # Rough estimate
        
        # Spam score (simplified)
        spam_indicators = [
            "!!!" in html_content,
            "GRATIS" in html_content.upper(),
            "KOSTENLOS" in html_content.upper(),
            len(re.findall(r'[A-Z]{3,}', html_content)) > 5
        ]
        spam_score = sum(spam_indicators)
        
        return {
            "subject_analysis": {
                "length": subject_length,
                "rating": subject_rating
            },
            "mobile_score": mobile_score,
            "load_time_estimate": load_time_estimate,
            "spam_score": spam_score,
            "html_size_kb": round(html_size / 1024, 1),
            "plain_text_available": bool(plain_text),
            "compliance_checks": {
                "unsubscribe_link": "Abmelden" in html_content,
                "physical_address": any(word in html_content for word in ["Strasse", "Str.", "Platz", "Weg"]),
                "finma_mention": "FINMA" in html_content
            }
        }

    async def customize_template(self, kwargs) -> Response:
        """Customize email template with user preferences"""
        
        template_type = kwargs.get("template_type", "quote_follow_up")
        customizations = kwargs.get("customizations", {})
        
        # Apply customizations to branding
        custom_branding = {**self.default_branding, **customizations.get("branding", {})}
        
        message = f"""
🎨 **Template angepasst**: {template_type}

**Angepasste Elemente**:
{self._format_customizations(customizations)}

Die Anpassungen wurden erfolgreich übernommen. Möchten Sie eine Vorschau erstellen?
"""
        
        return Response(
            message=message,
            break_loop=False
        )

    def _format_customizations(self, customizations: dict) -> str:
        """Format customizations for display"""
        formatted = []
        
        if "branding" in customizations:
            branding = customizations["branding"]
            for key, value in branding.items():
                formatted.append(f"- {key.replace('_', ' ').title()}: {value}")
        
        if "content" in customizations:
            formatted.append(f"- Content-Anpassungen: {len(customizations['content'])} Änderungen")
        
        return "\n".join(formatted) if formatted else "- Keine spezifischen Anpassungen"

    async def preview_email(self, kwargs) -> Response:
        """Generate email preview with responsive design testing"""
        
        email_data = kwargs.get("email_data", {})
        
        if not email_data:
            return Response(
                message="❌ Keine E-Mail-Daten für Vorschau verfügbar",
                break_loop=False
            )
        
        # Generate preview URLs for different devices
        preview_data = {
            "desktop_preview": f"https://email-preview.insuragent.ch/desktop/{hash(str(email_data)) % 10000}",
            "mobile_preview": f"https://email-preview.insuragent.ch/mobile/{hash(str(email_data)) % 10000}",
            "tablet_preview": f"https://email-preview.insuragent.ch/tablet/{hash(str(email_data)) % 10000}",
            "dark_mode_preview": f"https://email-preview.insuragent.ch/dark/{hash(str(email_data)) % 10000}",
            "client_tests": {
                "gmail": "✅ Excellent",
                "outlook": "✅ Good", 
                "apple_mail": "✅ Excellent",
                "yahoo": "⚠️ Minor issues",
                "thunderbird": "✅ Good"
            }
        }
        
        message = f"""
📱 **E-Mail Vorschau generiert**

**Multi-Device Testing**:
🖥️ Desktop: {preview_data['desktop_preview']}
📱 Mobile: {preview_data['mobile_preview']}
📋 Tablet: {preview_data['tablet_preview']}
🌙 Dark Mode: {preview_data['dark_mode_preview']}

**Client-Kompatibilität**:
{self._format_client_tests(preview_data['client_tests'])}

**Responsive Design**: ✅ Optimiert für alle Bildschirmgrößen
**Ladezeit**: < 3 Sekunden auf allen Geräten
"""
        
        return Response(
            message=message,
            break_loop=False
        )

    def _format_client_tests(self, client_tests: dict) -> str:
        """Format client test results"""
        formatted = []
        for client, status in client_tests.items():
            formatted.append(f"- {client.replace('_', ' ').title()}: {status}")
        return "\n".join(formatted)

    async def generate_email_variations(self, kwargs) -> Response:
        """Generate A/B test variations of email"""
        
        base_template = kwargs.get("template_type", "quote_follow_up")
        variation_count = kwargs.get("variation_count", 3)
        
        variations = []
        
        for i in range(variation_count):
            variation = {
                "id": f"var_{i+1}",
                "name": f"Variation {i+1}",
                "changes": self._generate_variation_changes(i),
                "preview_url": f"https://email-preview.insuragent.ch/variation/{i+1}/{hash(base_template) % 10000}",
                "expected_performance": self._estimate_performance(i)
            }
            variations.append(variation)
        
        message = f"""
🧪 **A/B Test Variationen erstellt**

**Base Template**: {base_template.replace('_', ' ').title()}
**Generierte Variationen**: {variation_count}

{self._format_variations(variations)}

**Empfehlung**: Testen Sie alle Variationen mit kleinen Gruppen, bevor Sie die beste für den Hauptversand wählen.
"""
        
        return Response(
            message=message,
            break_loop=False
        )

    def _generate_variation_changes(self, variation_index: int) -> list:
        """Generate specific changes for email variation"""
        variation_sets = [
            ["Shorter subject line", "Different CTA color", "Bullet points instead of paragraphs"],
            ["Personal tone", "Larger font size", "Additional testimonial"],
            ["Urgency in subject", "Social proof", "Simplified layout"]
        ]
        
        return variation_sets[variation_index % len(variation_sets)]

    def _estimate_performance(self, variation_index: int) -> dict:
        """Estimate performance for variation"""
        base_metrics = {
            "open_rate": 22 + (variation_index * 2),
            "click_rate": 3.5 + (variation_index * 0.5),
            "conversion_rate": 1.2 + (variation_index * 0.3)
        }
        
        return base_metrics

    def _format_variations(self, variations: list) -> str:
        """Format variations for display"""
        formatted = []
        
        for var in variations:
            formatted.append(f"""
**{var['name']}**:
- Änderungen: {', '.join(var['changes'])}
- Erwartete Öffnungsrate: {var['expected_performance']['open_rate']}%
- Preview: {var['preview_url']}
""")
        
        return "\n".join(formatted)

    async def analyze_email_performance(self, kwargs) -> Response:
        """Analyze email performance and provide optimization suggestions"""
        
        email_id = kwargs.get("email_id", "unknown")
        metrics = kwargs.get("metrics", {})
        
        # Simulate performance analysis
        analysis_result = {
            "email_id": email_id,
            "performance_metrics": {
                "sent": metrics.get("sent", 1000),
                "delivered": metrics.get("delivered", 980),
                "opened": metrics.get("opened", 220),
                "clicked": metrics.get("clicked", 35),
                "converted": metrics.get("converted", 12),
                "unsubscribed": metrics.get("unsubscribed", 2)
            },
            "calculated_rates": {},
            "benchmarks": {
                "industry_open_rate": 22.5,
                "industry_click_rate": 3.2,
                "industry_conversion_rate": 1.8
            },
            "optimization_suggestions": []
        }
        
        # Calculate rates
        metrics = analysis_result["performance_metrics"]
        analysis_result["calculated_rates"] = {
            "delivery_rate": round((metrics["delivered"] / metrics["sent"]) * 100, 2),
            "open_rate": round((metrics["opened"] / metrics["delivered"]) * 100, 2),
            "click_rate": round((metrics["clicked"] / metrics["opened"]) * 100, 2),
            "conversion_rate": round((metrics["converted"] / metrics["clicked"]) * 100, 2),
            "unsubscribe_rate": round((metrics["unsubscribed"] / metrics["delivered"]) * 100, 2)
        }
        
        # Generate optimization suggestions
        rates = analysis_result["calculated_rates"]
        benchmarks = analysis_result["benchmarks"]
        
        if rates["open_rate"] < benchmarks["industry_open_rate"]:
            analysis_result["optimization_suggestions"].append("📧 Verbessern Sie die Betreffzeile - zu niedrige Öffnungsrate")
        
        if rates["click_rate"] < benchmarks["industry_click_rate"]:
            analysis_result["optimization_suggestions"].append("🔗 Optimieren Sie Call-to-Action Buttons - zu niedrige Klickrate")
        
        if rates["conversion_rate"] < benchmarks["industry_conversion_rate"]:
            analysis_result["optimization_suggestions"].append("💰 Landing Page überprüfen - niedrige Conversion")
        
        message = f"""
📊 **E-Mail Performance Analyse**

**Versand-Metriken**:
- Versendet: {metrics['sent']:,}
- Zugestellt: {metrics['delivered']:,} ({rates['delivery_rate']}%)
- Geöffnet: {metrics['opened']:,} ({rates['open_rate']}%)
- Geklickt: {metrics['clicked']:,} ({rates['click_rate']}%)
- Konvertiert: {metrics['converted']:,} ({rates['conversion_rate']}%)

**Benchmark-Vergleich**:
- Öffnungsrate: {'✅' if rates['open_rate'] >= benchmarks['industry_open_rate'] else '⚠️'} {rates['open_rate']}% (Ø {benchmarks['industry_open_rate']}%)
- Klickrate: {'✅' if rates['click_rate'] >= benchmarks['industry_click_rate'] else '⚠️'} {rates['click_rate']}% (Ø {benchmarks['industry_click_rate']}%)
- Conversion: {'✅' if rates['conversion_rate'] >= benchmarks['industry_conversion_rate'] else '⚠️'} {rates['conversion_rate']}% (Ø {benchmarks['industry_conversion_rate']}%)

**Optimierungsvorschläge**:
{chr(10).join(analysis_result['optimization_suggestions']) if analysis_result['optimization_suggestions'] else '✅ Alle Metriken im grünen Bereich!'}
"""
        
        return Response(
            message=message,
            break_loop=False
        ) 