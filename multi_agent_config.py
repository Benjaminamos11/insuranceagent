"""
Multi-Agent Configuration for Swiss Insurance Platform
Each agent has specialized roles and can delegate tasks to others
"""

import json
from typing import Dict, List, Any
from python.helpers.tool import Tool, Response

class MultiAgentOrchestrator:
    """
    Orchestrates multiple specialized agents for Swiss insurance tasks
    """
    
    def __init__(self):
        self.agents = {
            "project_manager": {
                "name": "Swiss Insurance Project Manager",
                "role": "Coordination and task management",
                "capabilities": [
                    "task_breakdown",
                    "workflow_coordination", 
                    "quality_control",
                    "agent_delegation"
                ],
                "prompt_file": "prompts/swiss_insurance/project_manager.md"
            },
            
            "research_analyst": {
                "name": "Swiss Insurance Research Analyst", 
                "role": "Market research and data analysis",
                "capabilities": [
                    "web_search",
                    "market_analysis",
                    "competitor_research", 
                    "finma_updates",
                    "screenshot_capture",
                    "data_visualization"
                ],
                "prompt_file": "prompts/swiss_insurance/research_analyst.md"
            },
            
            "content_creator": {
                "name": "Swiss Insurance Content Creator",
                "role": "Professional content and design creation", 
                "capabilities": [
                    "email_design",
                    "web_page_creation",
                    "social_media_content",
                    "visual_design",
                    "finma_compliance_check"
                ],
                "prompt_file": "prompts/swiss_insurance/content_creator.md",
                "tools": [
                    "EmailDesigner",
                    "WebPageBuilder", 
                    "SocialMediaCreator"
                ]
            },
            
            "consultation_expert": {
                "name": "Swiss Insurance Consultation Expert",
                "role": "Client consultation and insurance advice",
                "capabilities": [
                    "insurance_advice",
                    "policy_comparison",
                    "risk_assessment", 
                    "client_communication",
                    "finma_compliance"
                ],
                "prompt_file": "prompts/swiss_insurance/consultation_expert.md"
            }
        }
        
        # Workflow templates for common tasks
        self.workflows = {
            "email_campaign": {
                "description": "Create professional email campaign",
                "steps": [
                    {"agent": "project_manager", "task": "analyze_requirements"},
                    {"agent": "research_analyst", "task": "market_research"},
                    {"agent": "content_creator", "task": "create_email"},
                    {"agent": "consultation_expert", "task": "compliance_review"},
                    {"agent": "project_manager", "task": "final_review"}
                ]
            },
            
            "landing_page": {
                "description": "Create conversion-optimized landing page",
                "steps": [
                    {"agent": "project_manager", "task": "define_objectives"},
                    {"agent": "research_analyst", "task": "competitor_analysis"},
                    {"agent": "content_creator", "task": "design_page"},
                    {"agent": "consultation_expert", "task": "insurance_accuracy_check"},
                    {"agent": "project_manager", "task": "performance_optimization"}
                ]
            },
            
            "social_media_campaign": {
                "description": "Multi-platform social media campaign",
                "steps": [
                    {"agent": "project_manager", "task": "campaign_planning"},
                    {"agent": "research_analyst", "task": "audience_analysis"},
                    {"agent": "content_creator", "task": "create_content"},
                    {"agent": "consultation_expert", "task": "finma_compliance"},
                    {"agent": "project_manager", "task": "scheduling_optimization"}
                ]
            },
            
            "client_consultation": {
                "description": "Comprehensive client consultation",
                "steps": [
                    {"agent": "project_manager", "task": "consultation_planning"},
                    {"agent": "research_analyst", "task": "client_background_research"},
                    {"agent": "consultation_expert", "task": "insurance_consultation"},
                    {"agent": "content_creator", "task": "create_proposal"},
                    {"agent": "project_manager", "task": "follow_up_planning"}
                ]
            }
        }

    def route_request(self, request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Route incoming request to appropriate workflow and agents
        """
        
        # Analyze request to determine workflow
        request_lower = request.lower()
        
        if any(word in request_lower for word in ["email", "e-mail", "newsletter"]):
            workflow = "email_campaign"
        elif any(word in request_lower for word in ["website", "landing", "page", "web"]):
            workflow = "landing_page"
        elif any(word in request_lower for word in ["social", "facebook", "linkedin", "instagram"]):
            workflow = "social_media_campaign"
        elif any(word in request_lower for word in ["beratung", "consultation", "advice", "kunde"]):
            workflow = "client_consultation"
        else:
            # Default to project manager for analysis
            workflow = "general_analysis"
        
        return {
            "workflow": workflow,
            "primary_agent": self._get_primary_agent(workflow),
            "supporting_agents": self._get_supporting_agents(workflow),
            "estimated_steps": len(self.workflows.get(workflow, {}).get("steps", [])),
            "capabilities_needed": self._get_required_capabilities(workflow)
        }

    def _get_primary_agent(self, workflow: str) -> str:
        """Determine primary agent for workflow"""
        primary_mapping = {
            "email_campaign": "content_creator",
            "landing_page": "content_creator", 
            "social_media_campaign": "content_creator",
            "client_consultation": "consultation_expert",
            "general_analysis": "project_manager"
        }
        return primary_mapping.get(workflow, "project_manager")

    def _get_supporting_agents(self, workflow: str) -> List[str]:
        """Get supporting agents for workflow"""
        if workflow in self.workflows:
            steps = self.workflows[workflow]["steps"]
            return list(set(step["agent"] for step in steps))
        return ["project_manager", "research_analyst"]

    def _get_required_capabilities(self, workflow: str) -> List[str]:
        """Get required capabilities for workflow"""
        capability_mapping = {
            "email_campaign": ["email_design", "market_analysis", "finma_compliance"],
            "landing_page": ["web_page_creation", "competitor_research", "seo_optimization"],
            "social_media_campaign": ["social_media_content", "audience_analysis", "performance_tracking"],
            "client_consultation": ["insurance_advice", "risk_assessment", "policy_comparison"],
            "general_analysis": ["task_breakdown", "workflow_coordination"]
        }
        return capability_mapping.get(workflow, ["task_breakdown"])

# Initialize orchestrator
orchestrator = MultiAgentOrchestrator()

def route_insurance_request(request: str, context: Dict[str, Any] = None) -> str:
    """
    Main entry point for routing insurance agent requests
    """
    routing_info = orchestrator.route_request(request, context)
    
    response = f"""
🎯 **Request Analysis & Routing**

**Detected Workflow**: {routing_info['workflow'].replace('_', ' ').title()}
**Primary Agent**: {routing_info['primary_agent'].replace('_', ' ').title()}
**Supporting Agents**: {', '.join(agent.replace('_', ' ').title() for agent in routing_info['supporting_agents'])}

**🔧 Required Capabilities**:
{chr(10).join(f"- {cap.replace('_', ' ').title()}" for cap in routing_info['capabilities_needed'])}

**📋 Process Steps**: {routing_info['estimated_steps']} estimated steps

**🚀 Initiating workflow with specialized agents...**

---

**Available Agent Capabilities**:
- 🌐 **Web Research**: Real-time internet search, competitor analysis, market trends
- 👁️ **Vision & Screenshots**: Can analyze images, take website screenshots  
- 📧 **Email Creation**: Professional HTML emails with your corporate branding
- 🌐 **Web Development**: Responsive landing pages, quote forms, comparison tools
- 📱 **Social Media**: Platform-optimized content for LinkedIn, Facebook, Instagram
- ⚖️ **FINMA Compliance**: Automatic regulatory compliance checking
- 🎨 **Design Systems**: Corporate identity integration across all materials

**Next**: The system will automatically coordinate between agents to complete your request.
"""
    
    return response 