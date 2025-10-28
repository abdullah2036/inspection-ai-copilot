#!/bin/bash

echo "🔧 Setting up Offline Inspection AI Copilot..."
echo "================================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose found"

# Create data directory
mkdir -p data
echo "✅ Created data directory"

# Build and start containers
echo "🏗️  Building containers..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Pull and load the LLM model
echo "📥 Downloading AI model (this may take a few minutes)..."
docker exec ollama_llm ollama pull phi

echo ""
echo "✅ Setup complete!"
echo ""
echo "================================================"
echo "🌐 Access the app at: http://localhost:8501"
echo "================================================"
echo ""
echo "Useful commands:"
echo "  Stop:    docker-compose down"
echo "  Restart: docker-compose restart"
echo "  Logs:    docker-compose logs -f"
echo "  Model:   docker exec ollama_llm ollama list"
echo ""
echo "To use a different model (e.g., mistral):"
echo "  docker exec ollama_llm ollama pull mistral"
echo ""