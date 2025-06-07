# 🇨🇭 Schweizer Versicherung KI-Assistent

Ein hochmoderner KI-Assistent speziell für Schweizer Versicherungsagenten mit McKinsey-Level Analysefähigkeiten, Zahlungsintegration und MCP-Server-Funktionalität.

## 🎯 **Was ist das?**

Dieser KI-Assistent verwandelt jeden Versicherungsagenten in einen Schweizer Versicherungsexperten mit:

- **Bright, benutzerfreundliche deutsche Oberfläche** für Kunden
- **Vollständige Admin-Kontrolle** für Agenten
- **Zahlungsintegration** mit Stripe (CHF 29-199/Monat)
- **E-Mail-Automatisierung** mit professionellen Vorlagen
- **FINMA-konforme** Versicherungsvergleiche
- **MCP-Server-Integration** für E-Mails, Kalender, CRM

## 🚀 **Schnellstart**

### **1. Sofort testen (Docker)**
```bash
# Agent Zero mit Docker starten
docker pull frdel/agent-zero-run
docker run -p 50001:80 frdel/agent-zero-run

# Besuchen Sie:
# Admin: http://localhost:50001
# Client: http://localhost:50001/client.html
```

### **2. OpenAI API Key hinzufügen**
1. Gehen Sie zu **Settings** (Zahnrad-Symbol)
2. Fügen Sie Ihren OpenAI API Key hinzu
3. Speichern Sie die Einstellungen

### **3. Schweizer Versicherungsexperte aktivieren**
1. Kopieren Sie `config_swiss_insurance.env` als `.env`
2. Setzen Sie: `PROMPTS_SUBDIR=swiss_insurance`
3. Starten Sie den Server neu

## 🎨 **Zwei Interfaces**

### **👥 Client Interface** (`/client.html`)
**Für Ihre Kunden - Bright & Benutzerfreundlich**

![Client Interface](docs/client-interface-preview.png)

**Features:**
- ✅ Deutschsprachige, helle Oberfläche
- ✅ Quick Actions (Tarife vergleichen, Offerte, etc.)
- ✅ FINMA & Schweizer Qualitäts-Badges
- ✅ Automatische Zahlungsaufforderung nach 5 kostenlosen Nachrichten
- ✅ Mobile-optimiert für Kunden unterwegs
- ✅ Professionelle Versicherungsberatung

### **⚙️ Admin Interface** (`/admin` oder `/`)
**Für Sie - Vollständige Kontrolle**

**Features:**
- ✅ Alle Agent Zero Funktionen
- ✅ Chat-Management und Verlauf
- ✅ Einstellungen und Konfiguration
- ✅ Task-Scheduling
- ✅ Prompt-Anpassung
- ✅ MCP-Server-Management

## 💰 **Subscription-System**

### **Pläne:**
- **Basic**: CHF 29/Monat (100 Nachrichten)
- **Professional**: CHF 79/Monat (500 Nachrichten)
- **Enterprise**: CHF 199/Monat (Unbegrenzt)

### **Features nach Plan:**
| Feature | Basic | Professional | Enterprise |
|---------|-------|--------------|------------|
| KI-Nachrichten | 100/Monat | 500/Monat | Unbegrenzt |
| Tarifvergleiche | ✅ | ✅ | ✅ |
| E-Mail-Vorlagen | ✅ | ✅ | ✅ |
| Erweiterte Analysen | ❌ | ✅ | ✅ |
| MCP-Integration | ❌ | ✅ | ✅ |
| Custom Branding | ❌ | ❌ | ✅ |
| API-Zugang | ❌ | ❌ | ✅ |
| Dedicated Support | ❌ | ❌ | ✅ |

## 🛠️ **Verfügbare Tools**

### **📊 Versicherungsvergleich**
```python
# Beispiel: Mehrere Angebote vergleichen
quotes = [
    {"provider": "Zurich", "annual_premium": 1200, "coverages": {...}},
    {"provider": "AXA", "annual_premium": 1450, "coverages": {...}},
    {"provider": "Allianz", "annual_premium": 1100, "coverages": {...}}
]

result = await compare_rates(action="compare_quotes", quotes=quotes)
# Ergebnis: Detaillierte Analyse mit Empfehlungen
```

### **📧 E-Mail-Automatisierung (MCP)**
```python
# Automatische E-Mail-Erstellung
await send_email(
    to_email="kunde@example.ch",
    client_name="Max Muster", 
    template_type="quote_follow_up",
    template_data={
        "insurance_type": "Hausratversicherung",
        "quote_details": "CHF 850/Jahr mit Vollkasko"
    }
)
```

### **📈 McKinsey-Style Analysen**
- Situation-Complication-Question-Answer Framework
- Datengestützte Empfehlungen
- Visuelle Vergleichsmatrizen
- Compliance-Checks

## 🔌 **MCP-Server-Integration**

### **📧 E-Mail-Server**
**Features:**
- Automatisches E-Mail-Checking
- Sentiment-Analyse eingehender E-Mails
- Professionelle Antwortvorlagen
- Prioritätsbewertung

**Setup:**
```bash
# In .env
AGENT_EMAIL=ihr.email@gmail.com
AGENT_EMAIL_PASSWORD=ihr-app-passwort
EMAIL_MCP_ENABLED=true
```

### **📅 Kalender-Integration**
- Automatische Terminbuchung
- Meeting-Erinnerungen
- Verfügbarkeitsprüfung

### **📋 CRM-Integration**
- Lead-Management
- Kundendatenbank
- Follow-up-Tracking

## 🇨🇭 **Schweizer Spezifika**

### **FINMA-Compliance**
- Automatische Regulierungsprüfung
- Kantonale Bestimmungen (alle 26 Kantone)
- VVG- und AIA-Konformität

### **Mehrsprachigkeit**
- **Deutsch** (Standard)
- **Französisch** (Romandie)
- **Italienisch** (Tessin)
- **Englisch** (Expats)

### **Schweizer Anbieter-Datenbank**
```python
swiss_providers = {
    "zurich": {"rating": "A+", "market_share": 0.18},
    "axa": {"rating": "A+", "market_share": 0.15},
    "allianz": {"rating": "A+", "market_share": 0.12},
    "mobiliar": {"rating": "A+", "market_share": 0.09},
    # ... alle wichtigen Schweizer Anbieter
}
```

## 🚀 **Deployment**

### **Railway.app (Empfohlen)**
```bash
# 1. Repository zu Railway verbinden
# 2. Umgebungsvariablen setzen:
OPENAI_API_KEY=your_key
STRIPE_SECRET_KEY=your_stripe_key
PROMPTS_SUBDIR=swiss_insurance

# 3. Automatisches Deployment
# URL: https://your-app.railway.app
```

### **Custom Domain Setup**
```bash
# In Railway Dashboard:
# 1. Custom Domain hinzufügen: versicherung-ki.ch
# 2. SSL automatisch aktiviert
# 3. DNS-Einstellungen konfigurieren
```

## 📊 **Geschäftsmodell**

### **Zielgruppen:**
1. **Einzelne Versicherungsagenten** (Basic Plan)
2. **Versicherungsagenturen** (Professional Plan)
3. **Versicherungsunternehmen** (Enterprise Plan)

### **Umsatzpotential:**
- **100 Benutzer × CHF 79 = CHF 7.900/Monat**
- **1.000 Benutzer × CHF 79 = CHF 79.000/Monat**
- **Enterprise-Kunden**: CHF 2.000-10.000/Monat

### **Marktgröße Schweiz:**
- ~8.000 Versicherungsagenten
- ~500 Versicherungsunternehmen
- Marktpotential: CHF 10M+ ARR

## 🛡️ **Sicherheit & Compliance**

### **Datenschutz:**
- DSGVO-konform
- Schweizer Datenschutzgesetz
- Verschlüsselte Datenübertragung
- Lokale Datenspeicherung möglich

### **Sicherheitsfeatures:**
- JWT-Authentifizierung
- Rate Limiting
- Input-Validierung
- Audit-Logs

## 📚 **Verwendung**

### **1. Für Agenten (Admin Interface)**
```bash
# Tarife vergleichen
1. Laden Sie Versicherungsangebote hoch (PDF/Excel)
2. System analysiert automatisch 
3. Erhalten Sie McKinsey-Style Vergleich
4. Generieren Sie Kundenempfehlung

# E-Mails automatisieren
1. Konfigurieren Sie E-Mail-Integration
2. System überwacht Posteingang
3. Automatische Antwortvorschläge
4. Ein-Klick-Versendung
```

### **2. Für Kunden (Client Interface)**
```bash
# Einfache Beratung
1. Besuchen Sie /client.html
2. Wählen Sie Quick Action oder stellen Sie Frage
3. Erhalten Sie professionelle Beratung
4. Bei Bedarf: Upgrade für erweiterte Features
```

## 🔧 **Entwicklung & Anpassung**

### **Custom Prompts erstellen:**
```bash
# 1. Erstellen Sie neuen Prompt-Ordner
mkdir prompts/ihr_unternehmen

# 2. Kopieren Sie Basis-Prompts
cp -r prompts/swiss_insurance/* prompts/ihr_unternehmen/

# 3. Anpassen der Rolle
vim prompts/ihr_unternehmen/agent.system.main.role.md

# 4. Aktivieren
echo "PROMPTS_SUBDIR=ihr_unternehmen" >> .env
```

### **Neue Tools hinzufügen:**
```python
# python/tools/mein_tool.py
class MeinVersicherungsTool(Tool):
    async def execute(self, **kwargs):
        # Ihre Logik hier
        return Response(message="Ergebnis", data={})
```

### **MCP-Server erstellen:**
```python
# python/mcp_servers/mein_mcp_server.py
class MeinMCPServer:
    async def get_tools(self):
        return [{"name": "mein_tool", ...}]
    
    async def call_tool(self, tool_name, arguments):
        # Ihre Integration hier
        pass
```

## 🆘 **Support & Hilfe**

### **Häufige Probleme:**

**1. Client-Interface nicht verfügbar**
```bash
# Lösung: Direkte Datei-URL verwenden
http://localhost:50001/client.html
```

**2. E-Mail-Integration funktioniert nicht**
```bash
# Prüfen Sie Gmail App-Passwort
# 2FA muss aktiviert sein
# App-spezifisches Passwort generieren
```

**3. Zahlungen funktionieren nicht**
```bash
# Stripe-Keys prüfen
# Webhook-URLs konfigurieren
# Test-Modus vs. Live-Modus
```

### **Community & Resources:**
- **GitHub**: Vollständiger Quellcode
- **Discord**: Agent Zero Community
- **Documentation**: Detaillierte Anleitungen
- **YouTube**: Video-Tutorials

## 🎉 **Was macht dieses System besonders?**

### **1. Sofort einsatzbereit**
- Docker-Container starten → Funktioniert
- Keine komplizierte Installation
- Professionelle UI out-of-the-box

### **2. Schweizer Markt-fokussiert**
- FINMA-Compliance eingebaut
- Alle wichtigen Anbieter in Datenbank
- Mehrsprachigkeit für CH-Markt

### **3. Vollständiges Geschäftsmodell**
- Subscription-System integriert
- Automatische Zahlungsabwicklung
- Skalierbare Architektur

### **4. Enterprise-ready**
- MCP-Server-Integration
- E-Mail-Automatisierung
- CRM-Anbindung möglich

### **5. McKinsey-Level Qualität**
- Strukturierte Analysen
- Datengestützte Empfehlungen
- Professionelle Präsentationen

## 🚀 **Nächste Schritte**

1. **Testen Sie das System lokal**
2. **Konfigurieren Sie Ihre Branding**
3. **Fügen Sie Ihre API-Keys hinzu**
4. **Deployen Sie auf Railway.app**
5. **Beginnen Sie mit der Kundenakquise**

**Dieses System kann Ihr Versicherungsgeschäft revolutionieren! 🎯**

---

## 📞 **Kontakt**

Für Support, Anpassungen oder Enterprise-Lösungen:

📧 E-Mail: support@versicherung-ki.ch  
🌐 Website: https://versicherung-ki.ch  
💬 Discord: Agent Zero Community  

**Viel Erfolg mit Ihrem KI-gestützten Versicherungsgeschäft! 🇨🇭🤖💼** 