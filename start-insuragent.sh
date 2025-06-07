#!/bin/bash

echo "🇨🇭 Starting Swiss Insurance Agent (Insuragent) with Docker..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if .env file exists
if [ ! -f "docker.env" ]; then
    echo "⚠️  docker.env file not found. Creating template..."
    echo "Please edit docker.env with your API keys before running again."
    exit 1
fi

# Stop existing container if running
echo "🛑 Stopping existing Insuragent container..."
docker-compose -f docker-compose.swiss.yml down

# Pull latest image
echo "📥 Pulling latest Agent Zero image..."
docker pull frdel/agent-zero:latest

# Start the container
echo "🚀 Starting Insuragent..."
docker-compose -f docker-compose.swiss.yml --env-file docker.env up -d

# Show status
echo ""
echo "✅ Insuragent is starting up..."
echo ""
echo "🌐 Access your interfaces at:"
echo "   • Admin Dashboard:     http://localhost:5000/"
echo "   • Insuragent Login:    http://localhost:5000/login.html"
echo "   • Swiss Client:        http://localhost:5000/client.html"
echo "   • Workspace:           http://localhost:5000/workspace.html"
echo ""
echo "📊 Check status with: docker-compose -f docker-compose.swiss.yml logs -f"
echo "🛑 Stop with: docker-compose -f docker-compose.swiss.yml down"
echo ""

# Wait a moment and show logs
sleep 3
echo "📋 Recent logs:"
docker-compose -f docker-compose.swiss.yml logs --tail=20 