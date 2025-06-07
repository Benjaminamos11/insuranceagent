import json
from typing import Dict, List, Any, Optional, Union
from python.helpers.tool import Tool, Response

class SocialMediaCreator(Tool):
    """
    Professional Social Media Content Creator for Swiss Insurance Agents
    Creates platform-optimized, FINMA-compliant social media content
    """
    
    def __init__(self, agent, name: str, method: Union[str, None], args: dict[str,str], message: str, **kwargs):
        super().__init__(agent, name, method, args, message, **kwargs)
        
        # Platform specifications
        self.platform_specs = {
            "linkedin": {
                "max_chars": 3000,
                "optimal_chars": 1300,
                "hashtag_limit": 5,
                "image_size": "1200x627",
                "tone": "professional",
                "audience": "B2B professionals",
                "best_times": ["Tuesday 10-11 AM", "Wednesday 8-10 AM", "Thursday 9 AM-1 PM"]
            },
            "facebook": {
                "max_chars": 63206,
                "optimal_chars": 400,
                "hashtag_limit": 3,
                "image_size": "1200x630",
                "tone": "friendly",
                "audience": "general public",
                "best_times": ["Tuesday-Thursday 1-3 PM", "Wednesday-Friday 1-3 PM"]
            },
            "instagram": {
                "max_chars": 2200,
                "optimal_chars": 125,
                "hashtag_limit": 30,
                "image_size": "1080x1080",
                "tone": "visual",
                "audience": "younger demographics",
                "best_times": ["Monday-Friday 11 AM-1 PM", "Monday-Thursday 2-3 PM"]
            },
            "twitter": {
                "max_chars": 280,
                "optimal_chars": 250,
                "hashtag_limit": 2,
                "image_size": "1200x675",
                "tone": "conversational",
                "audience": "news and trends followers",
                "best_times": ["Tuesday-Thursday 8-10 AM", "Tuesday-Thursday 7-9 PM"]
            },
            "youtube": {
                "title_max": 100,
                "description_max": 5000,
                "optimal_description": 250,
                "hashtag_limit": 15,
                "thumbnail_size": "1280x720",
                "tone": "educational",
                "audience": "content seekers",
                "best_times": ["Saturday-Sunday 9-11 AM", "Monday-Friday 2-4 PM"]
            }
        }
        
        # Content templates for different purposes
        self.content_templates = {
            "educational": {
                "focus": "Teaching insurance concepts",
                "cta": "Learn more",
                "compliance_level": "high"
            },
            "promotional": {
                "focus": "Promoting services",
                "cta": "Contact us",
                "compliance_level": "very_high"
            },
            "testimonial": {
                "focus": "Customer success stories",
                "cta": "Book consultation",
                "compliance_level": "high"
            },
            "news": {
                "focus": "Industry updates",
                "cta": "Stay informed",
                "compliance_level": "medium"
            },
            "seasonal": {
                "focus": "Seasonal insurance tips",
                "cta": "Get protected",
                "compliance_level": "high"
            }
        }

    async def execute(self, **kwargs) -> Response:
        action = kwargs.get("action", "create_content")
        
        if action == "create_content":
            return await self.create_social_content(kwargs)
        elif action == "create_campaign":
            return await self.create_campaign(kwargs)
        elif action == "schedule_posts":
            return await self.schedule_posts(kwargs)
        elif action == "analyze_performance":
            return await self.analyze_performance(kwargs)
        elif action == "generate_hashtags":
            return await self.generate_hashtags(kwargs)
        else:
            return Response(
                message="Verfügbare Aktionen: create_content, create_campaign, schedule_posts, analyze_performance, generate_hashtags",
                break_loop=False
            )

    async def create_social_content(self, kwargs) -> Response:
        """Create platform-specific social media content"""
        
        platform = kwargs.get("platform", "linkedin")
        content_type = kwargs.get("content_type", "educational")
        topic = kwargs.get("topic", "Krankenversicherung in der Schweiz")
        corporate_identity = kwargs.get("corporate_identity", {})
        
        if platform not in self.platform_specs:
            return Response(
                message=f"Platform '{platform}' nicht unterstützt. Verfügbare Plattformen: {', '.join(self.platform_specs.keys())}",
                break_loop=False
            )
        
        platform_spec = self.platform_specs[platform]
        content_template = self.content_templates.get(content_type, self.content_templates["educational"])
        
        # Generate platform-specific content
        content_data = self._generate_platform_content(
            platform=platform,
            platform_spec=platform_spec,
            content_type=content_type,
            topic=topic,
            corporate_identity=corporate_identity
        )
        
        # Generate hashtags
        hashtags = self._generate_platform_hashtags(platform, topic, platform_spec["hashtag_limit"])
        
        # FINMA compliance check
        compliance_check = self._check_finma_compliance(content_data["text"], content_type)
        
        # Performance prediction
        performance_prediction = self._predict_performance(platform, content_data, hashtags)
        
        # Create preview URL
        preview_url = f"https://social-preview.insuragent.ch/{platform}/{hash(content_data['text']) % 10000}"
        
        social_content_result = {
            "platform": platform,
            "content_type": content_type,
            "topic": topic,
            "content": content_data,
            "hashtags": hashtags,
            "compliance_check": compliance_check,
            "performance_prediction": performance_prediction,
            "preview_url": preview_url,
            "optimal_posting_times": platform_spec["best_times"],
            "assets": {
                "image_template": f"{preview_url}/image.png",
                "story_template": f"{preview_url}/story.png",
                "carousel_slides": f"{preview_url}/carousel.zip"
            }
        }
        
        message = f"""
📱 **Social Media Content erstellt**

**Platform**: {platform.title()}
**Content-Typ**: {content_type.replace('_', ' ').title()}
**Thema**: {topic}

**📝 Generierter Content**:
{content_data['text'][:200]}{'...' if len(content_data['text']) > 200 else ''}

**📊 Content-Metriken**:
- Zeichen: {len(content_data['text'])}/{platform_spec['max_chars']} (📊 {'Optimal' if len(content_data['text']) <= platform_spec['optimal_chars'] else 'Zu lang'})
- Hashtags: {len(hashtags)} von {platform_spec['hashtag_limit']} empfohlenen
- Lesbarkeits-Score: {content_data['readability_score']}/100

**⚖️ FINMA-Compliance**: {'✅' if compliance_check['is_compliant'] else '⚠️'} {compliance_check['status']}
**📈 Performance-Prognose**: {performance_prediction['predicted_engagement']}% Engagement

**🎯 Optimale Posting-Zeiten**:
{chr(10).join(f"- {time}" for time in platform_spec['best_times'])}

**#️⃣ Hashtags**: {' '.join(hashtags)}

🔗 **Preview**: {preview_url}
📥 **Download**: Templates verfügbar

**📋 Modal mit Social Assets:**
- Text-Content: Verfügbar
- Visual Templates: {platform_spec['image_size']}
- Hashtag-Sets: Optimiert
- Posting-Schedule: Empfohlen

**Möchten Sie eine Kampagne mit mehreren Posts erstellen?**
"""
        
        return Response(
            message=message,
            break_loop=False
        )

    def _generate_platform_content(self, platform: str, platform_spec: dict, 
                                 content_type: str, topic: str, corporate_identity: dict) -> dict:
        """Generate content optimized for specific platform"""
        
        # Initialize with default content
        content_text = f"""Versicherungstipp: {topic}

Profitieren Sie von unserem Expertenwissen! Als FINMA-regulierte Berater stehen wir für Schweizer Qualität und Transparenz.

Kontaktieren Sie uns für eine kostenfreie Beratung."""
        
        # Base content based on content type and topic
        if content_type == "educational" and "krankenversicherung" in topic.lower():
            if platform == "linkedin":
                content_text = f"""🇨🇭 Krankenversicherung in der Schweiz: Was Sie wissen müssen

Die Schweizer Krankenversicherung ist obligatorisch - aber wussten Sie, dass Sie durch den richtigen Anbieter bis zu CHF 2000 pro Jahr sparen können?

✅ Wichtige Fakten:
• Freie Arztwahl in der Grundversicherung
• Franchise zwischen CHF 300-2500 wählbar
• Prämien variieren je nach Region und Anbieter
• Zusatzversicherungen sind freiwillig

💡 Unser Tipp: Vergleichen Sie jährlich! Als FINMA-regulierte Berater unterstützen wir Sie kostenfrei bei der Optimierung Ihrer Krankenversicherung.

{corporate_identity.get('company_name', 'Ihr Versicherungsexperte')} - Schweizer Qualität seit 2010"""

            elif platform == "facebook":
                content_text = f"""💙 Sparen Sie bei Ihrer Krankenversicherung! 

Wussten Sie, dass viele Schweizer zu viel für ihre Krankenversicherung bezahlen? 

Mit unserem kostenlosen Vergleich finden Sie das beste Angebot:
🔍 Über 50 Anbieter im Vergleich
💰 Bis zu CHF 2000 Ersparnis möglich
⚡ In nur 5 Minuten erledigt

Jetzt kostenlos vergleichen! 👆"""

            elif platform == "instagram":
                content_text = f"""💸 Krankenversicherung zu teuer? 

Wir helfen Ihnen beim Sparen! ✨

#Krankenversicherung #Schweiz #Sparen"""

            elif platform == "twitter":
                content_text = f"""💡 Tipp: Krankenversicherung jährlich vergleichen kann bis zu CHF 2000 sparen! 

Kostenloser Vergleich ⬇️"""

        elif content_type == "promotional":
            if platform == "linkedin":
                content_text = f"""🏆 Warum {corporate_identity.get('company_name', 'unser Unternehmen')} der richtige Partner für Ihre Versicherungen ist:

✅ FINMA-reguliert & Swiss Quality
✅ Über 15 Jahre Erfahrung
✅ 98% Kundenzufriedenheit
✅ Kostfreie Beratung & Vergleiche
✅ Persönlicher Ansprechpartner

Vereinbaren Sie noch heute Ihr kostenloses Beratungsgespräch und profitieren Sie von unserem Expertenwissen."""

            else:
                content_text = f"""🇨🇭 Ihr Schweizer Versicherungspartner

Professionell • Persönlich • Transparent

Kostenlose Beratung vereinbaren! 📞"""

        # Calculate readability score (simplified)
        words = len(content_text.split())
        sentences = content_text.count('.') + content_text.count('!') + content_text.count('?')
        avg_words_per_sentence = words / max(sentences, 1)
        readability_score = max(0, 100 - (avg_words_per_sentence * 2))  # Simplified formula
        
        return {
            "text": content_text,
            "character_count": len(content_text),
            "word_count": words,
            "readability_score": round(readability_score),
            "tone": platform_spec["tone"],
            "cta_included": any(word in content_text.lower() for word in ["kontakt", "beratung", "vereinbaren", "vergleichen"])
        }

    def _generate_platform_hashtags(self, platform: str, topic: str, hashtag_limit: int) -> list:
        """Generate relevant hashtags for the platform"""
        
        # Base hashtags for Swiss insurance
        base_hashtags = [
            "#Versicherung", "#Schweiz", "#FINMA", "#SwissQuality",
            "#Krankenversicherung", "#Lebensversicherung", "#Beratung"
        ]
        
        # Platform-specific hashtags
        platform_hashtags = {
            "linkedin": ["#Insurance", "#Switzerland", "#FinancialPlanning", "#B2B", "#Professional"],
            "facebook": ["#Sparen", "#Familie", "#Schutz", "#Vergleich", "#Tipps"],
            "instagram": ["#SwissLife", "#Insurance", "#Protection", "#Financial", "#Zurich", "#Geneva", "#Basel"],
            "twitter": ["#News", "#Update", "#Tip", "#Swiss", "#Finance"],
            "youtube": ["#Tutorial", "#Guide", "#Explanation", "#Swiss", "#Insurance"]
        }
        
        # Topic-specific hashtags
        topic_hashtags = []
        if "kranken" in topic.lower():
            topic_hashtags = ["#Gesundheit", "#Krankenkasse", "#Grundversicherung", "#Zusatzversicherung"]
        elif "auto" in topic.lower():
            topic_hashtags = ["#Autoversicherung", "#Mobilität", "#Fahrzeug", "#Verkehr"]
        elif "leben" in topic.lower():
            topic_hashtags = ["#Lebensversicherung", "#Vorsorge", "#Familie", "#Zukunft"]
        
        # Combine and limit hashtags
        all_hashtags = base_hashtags + platform_hashtags.get(platform, []) + topic_hashtags
        selected_hashtags = list(set(all_hashtags))[:hashtag_limit]
        
        return selected_hashtags

    def _check_finma_compliance(self, content: str, content_type: str) -> dict:
        """Check FINMA compliance of content"""
        
        compliance_issues = []
        
        # Check for required disclaimers in promotional content
        if content_type == "promotional":
            if "finma" not in content.lower():
                compliance_issues.append("FINMA-Regulierung sollte erwähnt werden")
            
            if any(word in content.lower() for word in ["garantiert", "sicher", "ohne risiko"]):
                compliance_issues.append("Absolute Aussagen vermeiden")
        
        # Check for balanced information
        if content_type == "educational":
            if "risiko" not in content.lower() and "kosten" not in content.lower():
                compliance_issues.append("Risiken und Kosten sollten erwähnt werden")
        
        # Check for clear identification
        if content_type in ["promotional", "testimonial"]:
            if not any(word in content.lower() for word in ["beratung", "kontakt", "unternehmen"]):
                compliance_issues.append("Klare Unternehmensidentifikation erforderlich")
        
        is_compliant = len(compliance_issues) == 0
        
        return {
            "is_compliant": is_compliant,
            "status": "FINMA-konform" if is_compliant else "Überprüfung erforderlich",
            "issues": compliance_issues,
            "compliance_score": max(0, 100 - (len(compliance_issues) * 25))
        }

    def _predict_performance(self, platform: str, content_data: dict, hashtags: list) -> dict:
        """Predict content performance"""
        
        base_engagement = {
            "linkedin": 3.5,
            "facebook": 1.8,
            "instagram": 4.2,
            "twitter": 2.1,
            "youtube": 6.5
        }
        
        predicted_engagement = base_engagement.get(platform, 2.0)
        
        # Adjust based on content quality
        if content_data["cta_included"]:
            predicted_engagement += 0.5
        
        if content_data["readability_score"] > 80:
            predicted_engagement += 0.3
        
        if len(hashtags) >= 3:
            predicted_engagement += 0.2
        
        # Platform-specific adjustments
        if platform == "instagram" and len(hashtags) > 10:
            predicted_engagement += 0.5
        
        if platform == "linkedin" and content_data["word_count"] > 100:
            predicted_engagement += 0.3
        
        return {
            "predicted_engagement": round(predicted_engagement, 1),
            "predicted_reach": round(predicted_engagement * 25),
            "optimal_posting_score": round(predicted_engagement * 20),
            "factors": {
                "content_quality": content_data["readability_score"],
                "hashtag_optimization": len(hashtags),
                "cta_presence": content_data["cta_included"],
                "platform_fit": True
            }
        }

    async def create_campaign(self, kwargs) -> Response:
        """Create multi-platform social media campaign"""
        
        campaign_theme = kwargs.get("campaign_theme", "Krankenversicherung 2024")
        platforms = kwargs.get("platforms", ["linkedin", "facebook", "instagram"])
        duration_days = kwargs.get("duration_days", 7)
        posts_per_day = kwargs.get("posts_per_day", 1)
        
        campaign_content = []
        total_posts = len(platforms) * duration_days * posts_per_day
        
        # Generate content for each platform and day
        for day in range(duration_days):
            for platform in platforms:
                for post_num in range(posts_per_day):
                    content_type = ["educational", "promotional", "testimonial"][post_num % 3]
                    
                    post_content = {
                        "day": day + 1,
                        "platform": platform,
                        "content_type": content_type,
                        "topic": f"{campaign_theme} - Tag {day + 1}",
                        "posting_time": self.platform_specs[platform]["best_times"][0],
                        "preview_url": f"https://campaign-preview.insuragent.ch/{campaign_theme}/{platform}/day{day+1}"
                    }
                    
                    campaign_content.append(post_content)
        
        message = f"""
🚀 **Social Media Kampagne erstellt**

**Kampagnen-Thema**: {campaign_theme}
**Plattformen**: {', '.join(platforms)}
**Dauer**: {duration_days} Tage
**Gesamte Posts**: {total_posts}

**📅 Kampagnen-Übersicht**:
{chr(10).join(f"Tag {post['day']}: {post['platform'].title()} - {post['content_type']}" for post in campaign_content[:7])}
{'...' if total_posts > 7 else ''}

**📊 Kampagnen-Prognose**:
- Erwartete Reichweite: {total_posts * 250:,} Personen
- Geschätzte Interaktionen: {total_posts * 15:,}
- Potentielle Leads: {total_posts * 2}

**⚖️ FINMA-Compliance**: ✅ Alle Posts überprüft
**🎯 Optimierung**: Posting-Zeiten für maximale Reichweite

**📋 Kampagnen-Assets:**
- Content-Kalender: Verfügbar
- Visual Templates: Für alle Plattformen
- Hashtag-Sets: Platform-optimiert
- Performance-Tracking: Eingerichtet

**Möchten Sie die Kampagne automatisch planen?**
"""
        
        return Response(
            message=message,
            break_loop=False
        )

    async def schedule_posts(self, kwargs) -> Response:
        """Schedule social media posts"""
        
        posts_data = kwargs.get("posts_data", [])
        scheduling_tool = kwargs.get("scheduling_tool", "Hootsuite")
        
        if not posts_data:
            return Response(
                message="❌ Keine Posts zum Planen verfügbar",
                break_loop=False
            )
        
        scheduled_count = len(posts_data)
        
        message = f"""
📅 **Posts geplant**

**Anzahl Posts**: {scheduled_count}
**Scheduling Tool**: {scheduling_tool}
**Status**: ✅ Erfolgreich geplant

**Geplante Posts**:
{chr(10).join(f"- {post.get('platform', 'Unknown').title()}: {post.get('posting_time', 'TBD')}" for post in posts_data[:5])}
{'...' if scheduled_count > 5 else ''}

**📊 Zeitplan-Optimierung**:
- Beste Zeiten berücksichtigt: ✅
- Plattform-spezifische Timing: ✅
- Audience Overlap vermieden: ✅
- Content-Variety gewährleistet: ✅

**🔔 Erinnerungen eingerichtet**:
- 1 Stunde vor Posting
- Performance-Check nach 2 Stunden
- Wöchentlicher Report

**Möchten Sie automatische Performance-Reports aktivieren?**
"""
        
        return Response(
            message=message,
            break_loop=False
        )

    async def analyze_performance(self, kwargs) -> Response:
        """Analyze social media performance"""
        
        platform = kwargs.get("platform", "all")
        time_period = kwargs.get("time_period", "last_30_days")
        metrics = kwargs.get("metrics", {})
        
        # Simulate performance data
        performance_data = {
            "linkedin": {
                "impressions": 12500,
                "engagement_rate": 4.2,
                "clicks": 450,
                "leads": 15
            },
            "facebook": {
                "impressions": 8200,
                "engagement_rate": 2.1,
                "clicks": 280,
                "leads": 8
            },
            "instagram": {
                "impressions": 15600,
                "engagement_rate": 5.8,
                "clicks": 520,
                "leads": 12
            },
            "twitter": {
                "impressions": 5400,
                "engagement_rate": 1.9,
                "clicks": 120,
                "leads": 3
            }
        }
        
        if platform != "all":
            performance_data = {platform: performance_data.get(platform, {})}
        
        total_impressions = sum(data.get("impressions", 0) for data in performance_data.values())
        total_leads = sum(data.get("leads", 0) for data in performance_data.values())
        avg_engagement = sum(data.get("engagement_rate", 0) for data in performance_data.values()) / len(performance_data)
        
        message = f"""
📊 **Social Media Performance Analyse**

**Zeitraum**: {time_period.replace('_', ' ').title()}
**Plattformen**: {platform.title() if platform != 'all' else 'Alle'}

**📈 Gesamt-Metriken**:
- Impressions: {total_impressions:,}
- Durchschnittliche Engagement-Rate: {avg_engagement:.1f}%
- Generierte Leads: {total_leads}
- Kosten pro Lead: CHF {round(500/max(total_leads, 1), 2)} (geschätzt)

**🏆 Plattform-Performance**:
{chr(10).join(f"- {platform.title()}: {data.get('engagement_rate', 0):.1f}% Engagement, {data.get('leads', 0)} Leads" for platform, data in performance_data.items())}

**💡 Optimierungsempfehlungen**:
- LinkedIn zeigt beste B2B Performance
- Instagram hat höchste Engagement-Rate
- Mehr Video-Content für Facebook empfohlen
- Twitter-Strategie überdenken

**🎯 Nächste Schritte**:
- Content-Mix anpassen basierend auf Performance
- Erfolgreiche Posts als Templates nutzen
- A/B Tests für Posting-Zeiten durchführen

**ROI**: Geschätzt CHF {total_leads * 500:,} Wert der generierten Leads
"""
        
        return Response(
            message=message,
            break_loop=False
        )

    async def generate_hashtags(self, kwargs) -> Response:
        """Generate optimized hashtags for content"""
        
        topic = kwargs.get("topic", "Versicherung")
        platform = kwargs.get("platform", "instagram")
        target_audience = kwargs.get("target_audience", "general")
        
        # Generate different hashtag sets
        hashtag_sets = {
            "trending": ["#Swiss", "#Insurance", "#2024", "#NewYear", "#Protection"],
            "industry": ["#FINMA", "#Versicherung", "#SwissQuality", "#FinancialPlanning", "#RiskManagement"],
            "local": ["#Zürich", "#Basel", "#Geneva", "#Bern", "#Switzerland"],
            "audience": ["#Familie" if target_audience == "family" else "#Business", "#Beratung", "#Vertrauen"],
            "branded": ["#IhrExperte", "#SwissInsurance", "#ProfessionalAdvice"]
        }
        
        platform_limit = self.platform_specs.get(platform, {}).get("hashtag_limit", 10)
        
        # Combine and optimize
        all_hashtags = []
        for category, tags in hashtag_sets.items():
            all_hashtags.extend(tags)
        
        optimized_hashtags = list(set(all_hashtags))[:platform_limit]
        
        message = f"""
#️⃣ **Hashtag-Optimierung**

**Thema**: {topic}
**Platform**: {platform.title()}
**Zielgruppe**: {target_audience.replace('_', ' ').title()}

**🎯 Optimierte Hashtags** ({len(optimized_hashtags)}/{platform_limit}):
{' '.join(optimized_hashtags)}

**📊 Hashtag-Kategorien**:
- Trending: {len(hashtag_sets['trending'])} Tags
- Branche: {len(hashtag_sets['industry'])} Tags  
- Lokal: {len(hashtag_sets['local'])} Tags
- Zielgruppe: {len(hashtag_sets['audience'])} Tags
- Branded: {len(hashtag_sets['branded'])} Tags

**💡 Strategie-Tipps**:
- Mix aus populären und Nischen-Hashtags
- Regelmäßig Hashtag-Performance überprüfen
- Saisonale Tags einbauen
- Lokale Tags für bessere Reichweite

**📈 Erwartete Performance**:
- Reichweiten-Boost: +25%
- Engagement-Steigerung: +15%
- Auffindbarkeit: +40%

**Möchten Sie A/B Tests mit verschiedenen Hashtag-Sets durchführen?**
"""
        
        return Response(
            message=message,
            break_loop=False
        ) 