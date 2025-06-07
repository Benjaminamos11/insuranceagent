from python.helpers.api import ApiHandler
from flask import Request, Response, redirect
from python.helpers import files
from typing import Union

class AdminDashboard(ApiHandler):
    """
    Admin Dashboard handler - provides access to full Agent Zero admin interface
    """
    
    @classmethod
    def requires_auth(cls) -> bool:
        return True
    
    async def process(self, input: dict, request: Request) -> Union[dict, Response]:
        # For GET requests, serve the admin interface
        if request.method == "GET":
            # Try to serve the original Agent Zero interface
            try:
                # Return the admin.html file we created
                admin_content = files.read_file("./webui/admin.html")
                return Response(
                    admin_content,
                    mimetype='text/html'
                )
            except Exception:
                # Fallback to redirect to root
                return redirect("/")
        
        # For other requests, return admin info
        return {
            "status": "admin_dashboard",
            "message": "Agent Zero Admin Dashboard",
            "features": [
                "API Configuration",
                "MCP Server Management", 
                "Swiss Insurance Settings",
                "Authentication Setup",
                "System Monitoring"
            ]
        } 