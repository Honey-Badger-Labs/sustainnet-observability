#!/bin/bash

# Local Grafana Setup Script for SustainNet Observability Demo
# This script sets up Grafana with sample data for dashboard preview

echo "🚀 Setting up SustainNet Observability Dashboards Locally"
echo "======================================================="

# Default Grafana credentials
GRAFANA_URL="http://localhost:3000"
GRAFANA_USER="admin"
GRAFANA_PASS="admin"

# Wait for Grafana to be ready
echo "⏳ Waiting for Grafana to be ready..."
sleep 5

# Test connection
if ! curl -s "$GRAFANA_URL/api/health" > /dev/null; then
    echo "❌ Grafana is not responding. Please make sure it's running:"
    echo "   brew services start grafana"
    exit 1
fi

echo "✅ Grafana is running"

# Change default password
echo "🔐 Updating default password..."
curl -s -X PUT "$GRAFANA_URL/api/user/password" \
    -H "Content-Type: application/json" \
    -d "{\"oldPassword\": \"admin\", \"newPassword\": \"sustainnet2026\"}" \
    --user "$GRAFANA_USER:$GRAFANA_PASS"

if [ $? -eq 0 ]; then
    echo "✅ Password updated to: sustainnet2026"
    GRAFANA_PASS="sustainnet2026"
else
    echo "⚠️  Password update failed, using default"
fi

# Create TestData data source for demo
echo "📊 Creating TestData data source..."
curl -s -X POST "$GRAFANA_URL/api/datasources" \
    -H "Content-Type: application/json" \
    --user "$GRAFANA_USER:$GRAFANA_PASS" \
    -d '{
        "name": "SustainNet Demo Data",
        "type": "testdata",
        "access": "proxy",
        "isDefault": true
    }'

echo "✅ TestData source created"

# Import Executive Summary Dashboard
echo "📈 Importing Executive Summary Dashboard..."
if [ -f "monitoring/executive-summary-dashboard.json" ]; then
    curl -s -X POST "$GRAFANA_URL/api/dashboards/db" \
        -H "Content-Type: application/json" \
        --user "$GRAFANA_USER:$GRAFANA_PASS" \
        -d "{\"dashboard\": $(cat monitoring/executive-summary-dashboard.json), \"overwrite\": true}"
    echo "✅ Executive Summary Dashboard imported"
else
    echo "❌ Executive Summary Dashboard file not found"
fi

# Import Infrastructure Dashboard
echo "🏗️  Importing Infrastructure Dashboard..."
if [ -f "monitoring/infrastructure-dashboard.json" ]; then
    curl -s -X POST "$GRAFANA_URL/api/dashboards/db" \
        -H "Content-Type: application/json" \
        --user "$GRAFANA_USER:$GRAFANA_PASS" \
        -d "{\"dashboard\": $(cat monitoring/infrastructure-dashboard.json), \"overwrite\": true}"
    echo "✅ Infrastructure Dashboard imported"
else
    echo "❌ Infrastructure Dashboard file not found"
fi

# Import CI/CD Dashboard
echo "🔄 Importing CI/CD Dashboard..."
if [ -f "monitoring/ci-cd-dashboard.json" ]; then
    curl -s -X POST "$GRAFANA_URL/api/dashboards/db" \
        -H "Content-Type: application/json" \
        --user "$GRAFANA_USER:$GRAFANA_PASS" \
        -d "{\"dashboard\": $(cat monitoring/ci-cd-dashboard.json), \"overwrite\": true}"
    echo "✅ CI/CD Dashboard imported"
else
    echo "❌ CI/CD Dashboard file not found"
fi

# Import Business Intelligence Dashboard
echo "💼 Importing Business Intelligence Dashboard..."
if [ -f "monitoring/business-intelligence-dashboard.json" ]; then
    curl -s -X POST "$GRAFANA_URL/api/dashboards/db" \
        -H "Content-Type: application/json" \
        --user "$GRAFANA_USER:$GRAFANA_PASS" \
        -d "{\"dashboard\": $(cat monitoring/business-intelligence-dashboard.json), \"overwrite\": true}"
    echo "✅ Business Intelligence Dashboard imported"
else
    echo "❌ Business Intelligence Dashboard file not found"
fi

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "🌐 Grafana URL: http://localhost:3000"
echo "👤 Username: admin"
echo "🔑 Password: sustainnet2026"
echo ""
echo "📊 Available Dashboards:"
echo "   • SustainNet Website - Executive Summary"
echo "   • SustainNet Website - Infrastructure Monitoring"
echo "   • SustainNet Website - CI/CD Pipeline"
echo "   • SustainNet Website - Business Intelligence"
echo ""
echo "💡 Tips:"
echo "   • Use the TestData source to see sample metrics"
echo "   • Dashboards will show simulated data for preview"
echo "   • Real AWS data will replace sample data when connected"
echo ""
echo "🔄 To restart fresh:"
echo "   brew services stop grafana"
echo "   rm -rf /opt/homebrew/var/lib/grafana/*"
echo "   brew services start grafana"
echo "   ./monitoring/setup-local-demo.sh"