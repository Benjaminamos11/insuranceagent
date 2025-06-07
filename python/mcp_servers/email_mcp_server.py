import asyncio
import json
import imaplib
import smtplib
import email
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from email.header import decode_header
from datetime import datetime, timedelta
from python.helpers import dotenv

class EmailMCPServer:
    """
    MCP Server for Email Integration
    Allows Agent Zero to check and send emails for insurance agents
    """
    
    def __init__(self):
        self.name = "email_server"
        self.version = "1.0.0"
        
        # Email configuration from environment
        self.email_config = {
            "smtp_server": dotenv.get_dotenv_value("SMTP_SERVER", "smtp.gmail.com"),
            "smtp_port": int(dotenv.get_dotenv_value("SMTP_PORT", "587")),
            "imap_server": dotenv.get_dotenv_value("IMAP_SERVER", "imap.gmail.com"),
            "imap_port": int(dotenv.get_dotenv_value("IMAP_PORT", "993")),
            "email": dotenv.get_dotenv_value("AGENT_EMAIL"),
            "password": dotenv.get_dotenv_value("AGENT_EMAIL_PASSWORD"),
            "use_tls": True
        }
        
        # Email templates for insurance
        self.email_templates = {
            "quote_follow_up": {
                "subject": "Ihr Versicherungsangebot - Haben Sie Fragen?",
                "template": """
Liebe/r {client_name},

vielen Dank für Ihr Interesse an unseren Versicherungslösungen.

Ich habe Ihnen ein personalisiertes Angebot für {insurance_type} erstellt:

{quote_details}

Falls Sie Fragen haben oder das Angebot besprechen möchten, können wir gerne einen Termin vereinbaren.

Mit freundlichen Grüssen,
{agent_name}
Versicherungsexperte

📞 {phone_number}
📧 {email}
🌐 {website}
"""
            },
            "claim_assistance": {
                "subject": "Schadensmeldung - Wir helfen Ihnen",
                "template": """
Liebe/r {client_name},

wir haben Ihre Schadensmeldung erhalten und werden uns umgehend darum kümmern.

Schadennummer: {claim_number}
Datum des Schadens: {incident_date}
Art des Schadens: {damage_type}

Nächste Schritte:
1. Unser Sachverständiger wird sich binnen 24 Stunden bei Ihnen melden
2. Bitte sammeln Sie alle relevanten Dokumente
3. Bei Fragen stehe ich Ihnen jederzeit zur Verfügung

Mit freundlichen Grüssen,
{agent_name}
"""
            },
            "policy_renewal": {
                "subject": "Verlängerung Ihrer Versicherungspolice",
                "template": """
Liebe/r {client_name},

Ihre Versicherungspolice {policy_number} läuft am {expiry_date} ab.

Ich habe Ihre Police überprüft und kann Ihnen folgende Optionen anbieten:
{renewal_options}

Vorteile einer frühzeitigen Verlängerung:
✓ Keine Unterbrechung des Versicherungsschutzes
✓ Mögliche Rabatte für treue Kunden
✓ Anpassung an neue Lebenssituationen

Lassen Sie uns einen Termin vereinbaren, um Ihre Bedürfnisse zu besprechen.

Mit freundlichen Grüssen,
{agent_name}
"""
            }
        }

    async def get_tools(self):
        """Return available email tools"""
        return [
            {
                "name": "check_emails",
                "description": "Check for new emails in the agent's inbox",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "hours_back": {
                            "type": "integer",
                            "description": "How many hours back to check for emails",
                            "default": 24
                        },
                        "filter_insurance": {
                            "type": "boolean", 
                            "description": "Only return emails related to insurance",
                            "default": True
                        }
                    }
                }
            },
            {
                "name": "send_email",
                "description": "Send a professional email to a client",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "to_email": {
                            "type": "string",
                            "description": "Recipient email address"
                        },
                        "client_name": {
                            "type": "string",
                            "description": "Client's name"
                        },
                        "template_type": {
                            "type": "string",
                            "enum": ["quote_follow_up", "claim_assistance", "policy_renewal", "custom"],
                            "description": "Type of email template to use"
                        },
                        "template_data": {
                            "type": "object",
                            "description": "Data to fill in the email template"
                        },
                        "custom_subject": {
                            "type": "string",
                            "description": "Custom subject line (for custom emails)"
                        },
                        "custom_body": {
                            "type": "string",
                            "description": "Custom email body (for custom emails)"
                        }
                    },
                    "required": ["to_email", "client_name", "template_type"]
                }
            },
            {
                "name": "analyze_email_sentiment",
                "description": "Analyze the sentiment and urgency of client emails",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "email_content": {
                            "type": "string",
                            "description": "Email content to analyze"
                        }
                    },
                    "required": ["email_content"]
                }
            },
            {
                "name": "create_email_summary",
                "description": "Create a summary of recent emails for daily review",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "period": {
                            "type": "string",
                            "enum": ["today", "yesterday", "week"],
                            "description": "Time period for email summary"
                        }
                    }
                }
            }
        ]

    async def call_tool(self, tool_name, arguments):
        """Execute the requested tool"""
        try:
            if tool_name == "check_emails":
                return await self.check_emails(**arguments)
            elif tool_name == "send_email":
                return await self.send_email(**arguments)
            elif tool_name == "analyze_email_sentiment":
                return await self.analyze_email_sentiment(**arguments)
            elif tool_name == "create_email_summary":
                return await self.create_email_summary(**arguments)
            else:
                return {"error": f"Unknown tool: {tool_name}"}
                
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}

    async def check_emails(self, hours_back=24, filter_insurance=True):
        """Check for new emails in the agent's inbox"""
        try:
            # Connect to IMAP server
            mail = imaplib.IMAP4_SSL(self.email_config["imap_server"], self.email_config["imap_port"])
            mail.login(self.email_config["email"], self.email_config["password"])
            mail.select("INBOX")
            
            # Calculate date filter
            since_date = (datetime.now() - timedelta(hours=hours_back)).strftime("%d-%b-%Y")
            
            # Search for emails
            status, messages = mail.search(None, f'SINCE "{since_date}"')
            email_ids = messages[0].split()
            
            emails = []
            insurance_keywords = [
                "versicherung", "insurance", "police", "schaden", "claim", 
                "prämie", "premium", "deckung", "coverage", "risiko", "risk"
            ]
            
            for email_id in email_ids[-20:]:  # Get last 20 emails
                status, msg_data = mail.fetch(email_id, "(RFC822)")
                
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        # Decode subject
                        subject = decode_header(msg["Subject"])[0][0]
                        if isinstance(subject, bytes):
                            subject = subject.decode()
                            
                        # Get sender
                        sender = msg.get("From")
                        
                        # Get body
                        body = self.get_email_body(msg)
                        
                        # Check if insurance-related
                        is_insurance_related = False
                        if filter_insurance:
                            content_to_check = f"{subject} {body}".lower()
                            is_insurance_related = any(keyword in content_to_check for keyword in insurance_keywords)
                        else:
                            is_insurance_related = True
                            
                        if is_insurance_related:
                            emails.append({
                                "id": email_id.decode(),
                                "sender": sender,
                                "subject": subject,
                                "body": body[:500] + "..." if len(body) > 500 else body,
                                "date": msg.get("Date"),
                                "urgency": self.assess_urgency(subject, body)
                            })
            
            mail.close()
            mail.logout()
            
            return {
                "success": True,
                "emails_found": len(emails),
                "emails": emails
            }
            
        except Exception as e:
            return {"error": f"Failed to check emails: {str(e)}"}

    async def send_email(self, to_email, client_name, template_type, template_data=None, custom_subject=None, custom_body=None):
        """Send a professional email to a client"""
        try:
            # Prepare email content
            if template_type == "custom":
                subject = custom_subject or "Nachricht von Ihrem Versicherungsberater"
                body = custom_body or ""
            else:
                template = self.email_templates.get(template_type)
                if not template:
                    return {"error": f"Unknown template type: {template_type}"}
                    
                subject = template["subject"]
                
                # Fill template with data
                template_data = template_data or {}
                template_data.update({
                    "client_name": client_name,
                    "agent_name": dotenv.get_dotenv_value("AGENT_NAME", "Ihr Versicherungsberater"),
                    "phone_number": dotenv.get_dotenv_value("AGENT_PHONE", "+41 XX XXX XX XX"),
                    "email": self.email_config["email"],
                    "website": dotenv.get_dotenv_value("AGENT_WEBSITE", "www.example.ch")
                })
                
                body = template["template"].format(**template_data)
            
            # Create email message
            msg = MimeMultipart()
            msg["From"] = self.email_config["email"]
            msg["To"] = to_email
            msg["Subject"] = subject
            
            # Add signature
            signature = f"""

---
{dotenv.get_dotenv_value("AGENT_NAME", "Ihr Versicherungsberater")}
Lizenzierter Versicherungsexperte

📞 {dotenv.get_dotenv_value("AGENT_PHONE", "+41 XX XXX XX XX")}
📧 {self.email_config["email"]}
🌐 {dotenv.get_dotenv_value("AGENT_WEBSITE", "www.example.ch")}

🛡️ FINMA reguliert | 🇨🇭 Schweizer Qualität
"""
            
            body_with_signature = body + signature
            msg.attach(MimeText(body_with_signature, "plain", "utf-8"))
            
            # Send email
            server = smtplib.SMTP(self.email_config["smtp_server"], self.email_config["smtp_port"])
            server.starttls()
            server.login(self.email_config["email"], self.email_config["password"])
            
            text = msg.as_string()
            server.sendmail(self.email_config["email"], to_email, text)
            server.quit()
            
            return {
                "success": True,
                "message": f"Email sent successfully to {to_email}",
                "subject": subject
            }
            
        except Exception as e:
            return {"error": f"Failed to send email: {str(e)}"}

    async def analyze_email_sentiment(self, email_content):
        """Analyze the sentiment and urgency of client emails"""
        # Simple sentiment analysis (in production, use proper NLP)
        urgent_keywords = ["dringend", "urgent", "sofort", "immediately", "asap", "notfall", "emergency"]
        negative_keywords = ["unzufrieden", "ärger", "problem", "beschwerde", "complaint", "disappointed"]
        positive_keywords = ["danke", "zufrieden", "excellent", "great", "perfect", "satisfied"]
        
        content_lower = email_content.lower()
        
        urgency = "low"
        sentiment = "neutral"
        
        # Check urgency
        if any(keyword in content_lower for keyword in urgent_keywords):
            urgency = "high"
        elif any(word in content_lower for word in ["bald", "soon", "heute", "today"]):
            urgency = "medium"
            
        # Check sentiment
        negative_count = sum(1 for keyword in negative_keywords if keyword in content_lower)
        positive_count = sum(1 for keyword in positive_keywords if keyword in content_lower)
        
        if negative_count > positive_count:
            sentiment = "negative"
        elif positive_count > negative_count:
            sentiment = "positive"
            
        return {
            "urgency": urgency,
            "sentiment": sentiment,
            "recommended_action": self.get_recommended_action(urgency, sentiment),
            "keywords_found": {
                "urgent": [kw for kw in urgent_keywords if kw in content_lower],
                "negative": [kw for kw in negative_keywords if kw in content_lower],
                "positive": [kw for kw in positive_keywords if kw in content_lower]
            }
        }

    async def create_email_summary(self, period="today"):
        """Create a summary of recent emails for daily review"""
        hours_map = {"today": 24, "yesterday": 48, "week": 168}
        hours_back = hours_map.get(period, 24)
        
        # Get emails
        email_check = await self.check_emails(hours_back=hours_back, filter_insurance=True)
        
        if not email_check.get("success"):
            return email_check
            
        emails = email_check["emails"]
        
        # Categorize emails
        urgent_emails = [e for e in emails if e.get("urgency") == "high"]
        new_inquiries = [e for e in emails if any(word in e["subject"].lower() for word in ["anfrage", "quote", "offer"])]
        claims = [e for e in emails if any(word in e["subject"].lower() for word in ["schaden", "claim"])]
        
        summary = {
            "period": period,
            "total_emails": len(emails),
            "urgent_emails": len(urgent_emails),
            "new_inquiries": len(new_inquiries),
            "claims": len(claims),
            "categories": {
                "urgent": [{"sender": e["sender"], "subject": e["subject"]} for e in urgent_emails],
                "inquiries": [{"sender": e["sender"], "subject": e["subject"]} for e in new_inquiries],
                "claims": [{"sender": e["sender"], "subject": e["subject"]} for e in claims]
            },
            "action_items": []
        }
        
        # Generate action items
        if urgent_emails:
            summary["action_items"].append(f"Prioritize {len(urgent_emails)} urgent emails")
        if new_inquiries:
            summary["action_items"].append(f"Follow up on {len(new_inquiries)} new inquiries")
        if claims:
            summary["action_items"].append(f"Process {len(claims)} insurance claims")
            
        return summary

    def get_email_body(self, msg):
        """Extract email body from message"""
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode()
                        break
                    except:
                        continue
        else:
            try:
                body = msg.get_payload(decode=True).decode()
            except:
                body = str(msg.get_payload())
                
        return body.strip()

    def assess_urgency(self, subject, body):
        """Assess the urgency level of an email"""
        urgent_indicators = ["dringend", "urgent", "sofort", "notfall", "emergency"]
        content = f"{subject} {body}".lower()
        
        if any(indicator in content for indicator in urgent_indicators):
            return "high"
        elif any(word in content for word in ["bald", "heute", "soon", "today"]):
            return "medium"
        else:
            return "low"

    def get_recommended_action(self, urgency, sentiment):
        """Get recommended action based on urgency and sentiment"""
        if urgency == "high":
            return "Contact client immediately within 2 hours"
        elif sentiment == "negative":
            return "Schedule a call to address concerns"
        elif sentiment == "positive":
            return "Send thank you note and check for referral opportunities"
        else:
            return "Respond within 24 hours with helpful information"

# Create the MCP server instance
email_mcp_server = EmailMCPServer() 