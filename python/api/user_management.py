import json
import bcrypt
import jwt
import stripe
import os
from datetime import datetime, timedelta
from python.helpers.api import ApiHandler
from python.helpers import dotenv

# Load Stripe configuration
stripe.api_key = dotenv.get_dotenv_value("STRIPE_SECRET_KEY")

class UserManagementApi(ApiHandler):
    """
    Handles user registration, authentication, and subscription management
    """
    
    def __init__(self, app, lock):
        super().__init__(app, lock)
        self.users_db = {}  # In production: use proper database
        self.active_sessions = {}
        
        # Subscription plans
        self.plans = {
            "basic": {
                "price_id": "price_basic_chf29",
                "price": 29,
                "currency": "chf",
                "messages_limit": 100,
                "features": ["basic_comparison", "email_templates"]
            },
            "professional": {
                "price_id": "price_professional_chf79", 
                "price": 79,
                "currency": "chf",
                "messages_limit": 500,
                "features": ["all_tools", "advanced_analysis", "priority_support"]
            },
            "enterprise": {
                "price_id": "price_enterprise_chf199",
                "price": 199,
                "currency": "chf", 
                "messages_limit": -1,  # Unlimited
                "features": ["custom_branding", "api_access", "dedicated_support"]
            }
        }

    async def handle_request(self, request):
        """Handle all user management requests"""
        try:
            if request.method == "POST":
                data = await request.get_json()
                action = data.get("action")
                
                if action == "register":
                    return await self.register_user(data)
                elif action == "login":
                    return await self.login_user(data)
                elif action == "create_checkout":
                    return await self.create_checkout_session(data)
                elif action == "verify_subscription":
                    return await self.verify_subscription(data)
                elif action == "check_usage":
                    return await self.check_usage_limits(data)
                    
            return {"error": "Invalid action"}, 400
            
        except Exception as e:
            return {"error": str(e)}, 500

    async def register_user(self, data):
        """Register a new user"""
        email = data.get("email")
        password = data.get("password")
        name = data.get("name")
        
        if not email or not password:
            return {"error": "Email and password required"}, 400
            
        # Check if user already exists
        if email in self.users_db:
            return {"error": "User already exists"}, 409
            
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create user
        user = {
            "id": len(self.users_db) + 1,
            "email": email,
            "name": name,
            "password_hash": password_hash.decode('utf-8'),
            "created_at": datetime.now().isoformat(),
            "subscription": {
                "plan": "free",
                "status": "active",
                "messages_used": 0,
                "messages_limit": 5,
                "period_start": datetime.now().isoformat()
            },
            "usage_stats": {
                "total_messages": 0,
                "last_activity": datetime.now().isoformat()
            }
        }
        
        self.users_db[email] = user
        
        # Generate JWT token
        token = self.generate_jwt_token(user)
        
        return {
            "success": True,
            "user": {
                "id": user["id"],
                "email": user["email"],
                "name": user["name"],
                "subscription": user["subscription"]
            },
            "token": token
        }

    async def login_user(self, data):
        """Authenticate user login"""
        email = data.get("email")
        password = data.get("password")
        
        if not email or not password:
            return {"error": "Email and password required"}, 400
            
        user = self.users_db.get(email)
        if not user:
            return {"error": "Invalid credentials"}, 401
            
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user["password_hash"].encode('utf-8')):
            return {"error": "Invalid credentials"}, 401
            
        # Update last activity
        user["usage_stats"]["last_activity"] = datetime.now().isoformat()
        
        # Generate JWT token
        token = self.generate_jwt_token(user)
        
        return {
            "success": True,
            "user": {
                "id": user["id"],
                "email": user["email"],
                "name": user["name"],
                "subscription": user["subscription"]
            },
            "token": token
        }

    async def create_checkout_session(self, data):
        """Create Stripe checkout session for subscription"""
        plan_type = data.get("plan")
        user_email = data.get("user_email")
        
        if plan_type not in self.plans:
            return {"error": "Invalid plan"}, 400
            
        plan = self.plans[plan_type]
        
        try:
            # Create Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': plan["price_id"],
                    'quantity': 1,
                }],
                mode='subscription',
                customer_email=user_email,
                success_url=f"{os.getenv('BASE_URL', 'http://localhost:50001')}/client.html?success=true",
                cancel_url=f"{os.getenv('BASE_URL', 'http://localhost:50001')}/client.html?cancelled=true",
                metadata={
                    'plan_type': plan_type,
                    'user_email': user_email
                }
            )
            
            return {
                "checkout_url": checkout_session.url,
                "session_id": checkout_session.id
            }
            
        except Exception as e:
            return {"error": f"Payment setup failed: {str(e)}"}, 500

    async def verify_subscription(self, data):
        """Verify and update user subscription status"""
        session_id = data.get("session_id")
        
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            
            if session.payment_status == "paid":
                user_email = session.metadata.get("user_email")
                plan_type = session.metadata.get("plan_type")
                
                if user_email in self.users_db:
                    plan = self.plans[plan_type]
                    
                    # Update user subscription
                    self.users_db[user_email]["subscription"] = {
                        "plan": plan_type,
                        "status": "active",
                        "messages_used": 0,
                        "messages_limit": plan["messages_limit"],
                        "period_start": datetime.now().isoformat(),
                        "stripe_session_id": session_id
                    }
                    
                    return {
                        "success": True,
                        "subscription": self.users_db[user_email]["subscription"]
                    }
                    
            return {"error": "Payment verification failed"}, 400
            
        except Exception as e:
            return {"error": f"Verification failed: {str(e)}"}, 500

    async def check_usage_limits(self, data):
        """Check if user has reached usage limits"""
        user_email = data.get("user_email")
        
        if user_email not in self.users_db:
            return {"error": "User not found"}, 404
            
        user = self.users_db[user_email]
        subscription = user["subscription"]
        
        # Check message limits
        messages_used = subscription["messages_used"]
        messages_limit = subscription["messages_limit"]
        
        can_send = True
        if messages_limit > 0 and messages_used >= messages_limit:
            can_send = False
            
        return {
            "can_send_message": can_send,
            "messages_used": messages_used,
            "messages_limit": messages_limit,
            "plan": subscription["plan"],
            "upgrade_required": not can_send
        }

    def increment_usage(self, user_email):
        """Increment message usage for user"""
        if user_email in self.users_db:
            self.users_db[user_email]["subscription"]["messages_used"] += 1
            self.users_db[user_email]["usage_stats"]["total_messages"] += 1
            self.users_db[user_email]["usage_stats"]["last_activity"] = datetime.now().isoformat()

    def generate_jwt_token(self, user):
        """Generate JWT token for user authentication"""
        secret_key = dotenv.get_dotenv_value("JWT_SECRET_KEY", "default_secret_key")
        
        payload = {
            "user_id": user["id"],
            "email": user["email"],
            "exp": datetime.utcnow() + timedelta(days=7)  # Token expires in 7 days
        }
        
        return jwt.encode(payload, secret_key, algorithm="HS256")

    def verify_jwt_token(self, token):
        """Verify JWT token and return user data"""
        try:
            secret_key = dotenv.get_dotenv_value("JWT_SECRET_KEY", "default_secret_key")
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def requires_auth():
        return False  # Open for registration

    @staticmethod
    def requires_loopback():
        return False  # Allow external access

    @staticmethod
    def requires_api_key():
        return False  # Use JWT instead 