#!/bin/bash

# Nepal Earthquake Damage Assessment - Setup Script
echo "🏔️ Setting up Nepal Earthquake Damage Assessment Project..."

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p data/raw
mkdir -p reports/figures
mkdir -p src/{data,visualization,models,utils}
mkdir -p tests
mkdir -p config
mkdir -p notebooks

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Generate sample data
echo "🏗️  Generating sample data..."
python src/data/generate_sample_data.py

echo "✅ Setup complete!"
echo "🚀 Run 'jupyter notebook' to start analyzing"
