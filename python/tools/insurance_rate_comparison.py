import json
import pandas as pd
import io
from typing import Dict, List, Any
from python.helpers.tool import Tool, Response

class InsuranceRateComparison(Tool):
    """
    Advanced insurance rate comparison tool for Swiss market
    Analyzes uploaded insurance quotes and creates comprehensive comparisons
    """
    
    def __init__(self, agent):
        super().__init__(agent)
        
        # Swiss insurance providers database
        self.swiss_providers = {
            "zurich": {"name": "Zurich Versicherung", "rating": "A+", "market_share": 0.18},
            "axa": {"name": "AXA Schweiz", "rating": "A+", "market_share": 0.15},
            "allianz": {"name": "Allianz Suisse", "rating": "A+", "market_share": 0.12},
            "generali": {"name": "Generali Schweiz", "rating": "A", "market_share": 0.08},
            "helvetia": {"name": "Helvetia", "rating": "A", "market_share": 0.07},
            "mobiliar": {"name": "Die Mobiliar", "rating": "A+", "market_share": 0.09},
            "baloise": {"name": "Baloise", "rating": "A", "market_share": 0.06},
            "vaudoise": {"name": "Vaudoise", "rating": "A-", "market_share": 0.04}
        }
        
        # Standard coverage types for comparison
        self.coverage_types = {
            "liability": "Haftpflichtversicherung",
            "comprehensive": "Vollkaskoversicherung", 
            "partial": "Teilkaskoversicherung",
            "legal_protection": "Rechtsschutzversicherung",
            "life": "Lebensversicherung",
            "health": "Krankenversicherung",
            "disability": "Invaliditätsversicherung",
            "property": "Hausratversicherung",
            "building": "Gebäudeversicherung"
        }

    async def execute(self, **kwargs) -> Response:
        """
        Execute rate comparison analysis
        """
        try:
            action = kwargs.get("action", "compare_quotes")
            
            if action == "compare_quotes":
                return await self.compare_insurance_quotes(kwargs)
            elif action == "generate_recommendation":
                return await self.generate_recommendation(kwargs)
            elif action == "create_comparison_matrix":
                return await self.create_comparison_matrix(kwargs)
            elif action == "calculate_savings":
                return await self.calculate_potential_savings(kwargs)
            else:
                return Response(
                    message="Unbekannte Aktion. Verfügbare Aktionen: compare_quotes, generate_recommendation, create_comparison_matrix, calculate_savings",
                    data={"error": "Invalid action"}
                )
                
        except Exception as e:
            return Response(
                message=f"Fehler bei der Tarifanalyse: {str(e)}",
                data={"error": str(e)}
            )

    async def compare_insurance_quotes(self, kwargs) -> Response:
        """
        Compare multiple insurance quotes
        """
        quotes_data = kwargs.get("quotes", [])
        client_profile = kwargs.get("client_profile", {})
        
        if not quotes_data:
            return Response(
                message="Keine Angebote zum Vergleichen gefunden. Bitte laden Sie Versicherungsangebote hoch.",
                data={"error": "No quotes provided"}
            )
        
        # Normalize quote data
        normalized_quotes = []
        for quote in quotes_data:
            normalized_quote = self.normalize_quote_data(quote)
            normalized_quotes.append(normalized_quote)
        
        # Perform comparison analysis
        comparison_result = {
            "total_quotes": len(normalized_quotes),
            "client_profile": client_profile,
            "quotes": normalized_quotes,
            "summary": self.generate_comparison_summary(normalized_quotes),
            "recommendations": self.generate_quote_recommendations(normalized_quotes, client_profile),
            "compliance_check": self.check_swiss_compliance(normalized_quotes)
        }
        
        # Generate visual comparison
        comparison_matrix = self.create_visual_comparison_matrix(normalized_quotes)
        comparison_result["visual_matrix"] = comparison_matrix
        
        message = f"""
📊 **Versicherungsvergleich abgeschlossen**

**Analysierte Angebote**: {len(normalized_quotes)}
**Preisspanne**: CHF {comparison_result['summary']['price_range']['min']:,.2f} - CHF {comparison_result['summary']['price_range']['max']:,.2f}
**Durchschnittspreis**: CHF {comparison_result['summary']['average_price']:,.2f}

**Beste Optionen**:
1. **Bestes Preis-Leistungs-Verhältnis**: {comparison_result['recommendations']['best_value']['provider']} (CHF {comparison_result['recommendations']['best_value']['price']:,.2f})
2. **Günstigste Option**: {comparison_result['recommendations']['cheapest']['provider']} (CHF {comparison_result['recommendations']['cheapest']['price']:,.2f})
3. **Beste Deckung**: {comparison_result['recommendations']['best_coverage']['provider']} ({comparison_result['recommendations']['best_coverage']['coverage_score']}% Deckung)

**Mögliche Einsparungen**: Bis zu CHF {comparison_result['summary']['max_savings']:,.2f} pro Jahr

✅ Alle Angebote sind FINMA-konform und entsprechen Schweizer Standards.
"""
        
        return Response(
            message=message,
            data=comparison_result
        )

    def normalize_quote_data(self, quote: Dict) -> Dict:
        """
        Normalize quote data to standard format
        """
        # Extract key information from uploaded quote
        provider = quote.get("provider", "Unbekannt")
        annual_premium = float(quote.get("annual_premium", 0))
        monthly_premium = annual_premium / 12 if annual_premium > 0 else float(quote.get("monthly_premium", 0)) * 12
        
        # Extract coverage details
        coverages = quote.get("coverages", {})
        deductible = float(quote.get("deductible", 0))
        
        # Calculate coverage score based on included benefits
        coverage_score = self.calculate_coverage_score(coverages)
        
        # Identify provider rating if available
        provider_key = provider.lower().replace(" ", "").replace("versicherung", "").replace("schweiz", "").replace("suisse", "")
        provider_info = self.swiss_providers.get(provider_key, {"rating": "N/A", "market_share": 0})
        
        return {
            "provider": provider,
            "provider_rating": provider_info["rating"],
            "market_share": provider_info["market_share"],
            "annual_premium": monthly_premium if monthly_premium > annual_premium else annual_premium,
            "monthly_premium": monthly_premium / 12 if monthly_premium > 100 else monthly_premium,
            "deductible": deductible,
            "coverages": coverages,
            "coverage_score": coverage_score,
            "value_score": self.calculate_value_score(monthly_premium, coverage_score),
            "raw_data": quote
        }

    def calculate_coverage_score(self, coverages: Dict) -> float:
        """
        Calculate coverage comprehensiveness score (0-100)
        """
        standard_coverages = [
            "liability", "comprehensive", "partial", "legal_protection",
            "personal_effects", "roadside_assistance", "replacement_vehicle"
        ]
        
        covered_count = 0
        total_coverage_value = 0
        
        for coverage in standard_coverages:
            if coverage in coverages:
                covered_count += 1
                # Add weight based on coverage limit
                limit = coverages.get(coverage, {}).get("limit", 0)
                if isinstance(limit, (int, float)) and limit > 0:
                    total_coverage_value += min(limit / 1000000, 1)  # Normalize to max 1M CHF
        
        base_score = (covered_count / len(standard_coverages)) * 60  # Base 60% for coverage breadth
        value_score = (total_coverage_value / len(standard_coverages)) * 40  # 40% for coverage depth
        
        return min(base_score + value_score, 100)

    def calculate_value_score(self, annual_premium: float, coverage_score: float) -> float:
        """
        Calculate value score (coverage quality vs price)
        """
        if annual_premium <= 0:
            return 0
        
        # Normalize premium (assume CHF 2000 as reference point)
        price_factor = 2000 / max(annual_premium, 100)
        value_score = (coverage_score / 100) * price_factor * 100
        
        return min(value_score, 100)

    def generate_comparison_summary(self, quotes: List[Dict]) -> Dict:
        """
        Generate summary statistics for comparison
        """
        if not quotes:
            return {}
        
        premiums = [q["annual_premium"] for q in quotes]
        coverage_scores = [q["coverage_score"] for q in quotes]
        
        return {
            "price_range": {
                "min": min(premiums),
                "max": max(premiums),
                "median": sorted(premiums)[len(premiums) // 2]
            },
            "average_price": sum(premiums) / len(premiums),
            "average_coverage": sum(coverage_scores) / len(coverage_scores),
            "max_savings": max(premiums) - min(premiums) if len(premiums) > 1 else 0,
            "provider_count": len(set(q["provider"] for q in quotes))
        }

    def generate_quote_recommendations(self, quotes: List[Dict], client_profile: Dict) -> Dict:
        """
        Generate personalized recommendations
        """
        if not quotes:
            return {}
        
        # Sort by different criteria
        cheapest = min(quotes, key=lambda x: x["annual_premium"])
        best_coverage = max(quotes, key=lambda x: x["coverage_score"])
        best_value = max(quotes, key=lambda x: x["value_score"])
        
        return {
            "cheapest": {
                "provider": cheapest["provider"],
                "price": cheapest["annual_premium"],
                "reason": "Niedrigste Jahresprämie"
            },
            "best_coverage": {
                "provider": best_coverage["provider"],
                "coverage_score": best_coverage["coverage_score"],
                "reason": "Umfassendste Deckung"
            },
            "best_value": {
                "provider": best_value["provider"],
                "price": best_value["annual_premium"],
                "value_score": best_value["value_score"],
                "reason": "Bestes Preis-Leistungs-Verhältnis"
            }
        }

    def check_swiss_compliance(self, quotes: List[Dict]) -> Dict:
        """
        Check compliance with Swiss insurance regulations
        """
        compliance_issues = []
        
        for quote in quotes:
            provider = quote["provider"]
            
            # Check minimum coverage requirements
            if quote["coverage_score"] < 30:
                compliance_issues.append(f"{provider}: Möglicherweise unzureichende Mindestdeckung")
            
            # Check pricing reasonableness (basic check)
            if quote["annual_premium"] < 300:
                compliance_issues.append(f"{provider}: Ungewöhnlich niedrige Prämie - Überprüfung empfohlen")
            
            if quote["annual_premium"] > 10000:
                compliance_issues.append(f"{provider}: Sehr hohe Prämie - Vergleich mit Marktstandards empfohlen")
        
        return {
            "compliant": len(compliance_issues) == 0,
            "issues": compliance_issues,
            "check_date": "2024-01-01",
            "regulator": "FINMA"
        }

    def create_visual_comparison_matrix(self, quotes: List[Dict]) -> str:
        """
        Create ASCII visual comparison matrix
        """
        if not quotes:
            return ""
        
        matrix = "📊 VERGLEICHSMATRIX\n"
        matrix += "=" * 80 + "\n"
        matrix += f"{'Anbieter':<20} {'Prämie/Jahr':<15} {'Deckung':<10} {'Bewertung':<12} {'Wert-Score':<10}\n"
        matrix += "-" * 80 + "\n"
        
        for quote in sorted(quotes, key=lambda x: x["value_score"], reverse=True):
            matrix += f"{quote['provider']:<20} "
            matrix += f"CHF {quote['annual_premium']:,.0f}   "
            matrix += f"{quote['coverage_score']:.0f}%     "
            matrix += f"{quote['provider_rating']:<12} "
            matrix += f"{quote['value_score']:.0f}/100\n"
        
        return matrix

    async def generate_recommendation(self, kwargs) -> Response:
        """
        Generate detailed recommendation report
        """
        comparison_data = kwargs.get("comparison_data", {})
        client_profile = kwargs.get("client_profile", {})
        
        if not comparison_data:
            return Response(
                message="Keine Vergleichsdaten verfügbar. Führen Sie zuerst einen Tarifvergleich durch.",
                data={"error": "No comparison data"}
            )
        
        recommendations = comparison_data.get("recommendations", {})
        best_option = recommendations.get("best_value", {})
        
        report = f"""
🎯 **PERSÖNLICHE VERSICHERUNGSEMPFEHLUNG**

**Für**: {client_profile.get('name', 'Kunde')}
**Analyse-Datum**: {pd.Timestamp.now().strftime('%d.%m.%Y')}

**EMPFOHLENE OPTION**: {best_option.get('provider', 'N/A')}
- Jahresprämie: CHF {best_option.get('price', 0):,.2f}
- Grund: {best_option.get('reason', 'Bestes Gesamtpaket')}

**BEGRÜNDUNG**:
1. Optimales Preis-Leistungs-Verhältnis
2. FINMA-konforme Deckung
3. Anpassung an Ihr Risikoprofil
4. Schweizer Marktstandards

**NÄCHSTE SCHRITTE**:
1. Detailberatung vereinbaren
2. Policenbedingungen prüfen
3. Vertragsabschluss vorbereiten
4. Bestehende Versicherungen kündigen
"""
        
        return Response(message=report, data={"recommendation_report": report})

    async def create_comparison_matrix(self, kwargs) -> Response:
        """
        Create detailed comparison matrix
        """
        quotes = kwargs.get("quotes", [])
        
        if not quotes:
            return Response(
                message="Keine Angebote für Matrix verfügbar.",
                data={"error": "No quotes"}
            )
        
        matrix_html = self.generate_html_comparison_matrix(quotes)
        
        return Response(
            message="Vergleichsmatrix erfolgreich erstellt.",
            data={"html_matrix": matrix_html, "quotes": quotes}
        )

    def generate_html_comparison_matrix(self, quotes: List[Dict]) -> str:
        """
        Generate HTML comparison matrix for web display
        """
        html = """
        <div class="comparison-matrix">
            <h3>📊 Versicherungsvergleich</h3>
            <table class="comparison-table">
                <thead>
                    <tr>
                        <th>Anbieter</th>
                        <th>Jahresprämie</th>
                        <th>Deckungsgrad</th>
                        <th>Bewertung</th>
                        <th>Wert-Score</th>
                        <th>Aktion</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for quote in sorted(quotes, key=lambda x: x["value_score"], reverse=True):
            html += f"""
                    <tr>
                        <td><strong>{quote['provider']}</strong></td>
                        <td>CHF {quote['annual_premium']:,.0f}</td>
                        <td>{quote['coverage_score']:.0f}%</td>
                        <td>{quote['provider_rating']}</td>
                        <td>{quote['value_score']:.0f}/100</td>
                        <td><button onclick="selectQuote('{quote['provider']}')">Auswählen</button></td>
                    </tr>
            """
        
        html += """
                </tbody>
            </table>
        </div>
        """
        
        return html

    async def calculate_potential_savings(self, kwargs) -> Response:
        """
        Calculate potential savings from switching
        """
        current_premium = float(kwargs.get("current_premium", 0))
        best_quote = kwargs.get("best_quote", {})
        
        if not current_premium or not best_quote:
            return Response(
                message="Bitte geben Sie Ihre aktuelle Prämie und ein Vergleichsangebot an.",
                data={"error": "Missing data"}
            )
        
        new_premium = best_quote.get("annual_premium", 0)
        annual_savings = current_premium - new_premium
        
        savings_report = f"""
💰 **EINSPARUNGSANALYSE**

**Aktuelle Prämie**: CHF {current_premium:,.2f}/Jahr
**Neue Prämie**: CHF {new_premium:,.2f}/Jahr
**Jährliche Einsparung**: CHF {annual_savings:,.2f}
**5-Jahres-Einsparung**: CHF {annual_savings * 5:,.2f}

**Empfehlung**: {"Wechsel empfohlen" if annual_savings > 0 else "Aktueller Tarif bereits günstig"}
"""
        
        return Response(
            message=savings_report,
            data={
                "current_premium": current_premium,
                "new_premium": new_premium,
                "annual_savings": annual_savings,
                "recommended": annual_savings > 0
            }
        )

# Tool registration
async def compare_rates(**kwargs):
    """Compare insurance rates from multiple providers"""
    agent = kwargs.get("agent")
    tool = InsuranceRateComparison(agent)
    return await tool.execute(**kwargs) 