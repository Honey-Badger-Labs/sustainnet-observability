#!/bin/bash

# Local Grafana Setup Script for SustainNet Observability Demo
# This script sets up Grafana with sample data for dashboard preview

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ENV_FILE="$ROOT/.env"

echo "🚀 Setting up SustainNet Observability Dashboards Locally"
echo "======================================================="

if [ ! -f "$ENV_FILE" ]; then
    echo "❌ No .env file found at $ENV_FILE"
    echo "   Copy the example and set your own passwords:"
    echo "   cp $ROOT/.env.example $ENV_FILE"
    exit 1
fi

set -a
# shellcheck disable=SC1090
. "$ENV_FILE"
set +a

GRAFANA_URL="${GRAFANA_URL:-http://localhost:3000}"
GRAFANA_USER="${GRAFANA_ADMIN_USER:-admin}"
: "${GRAFANA_ADMIN_PASSWORD:?Set GRAFANA_ADMIN_PASSWORD in .env (copy .env.example)}"

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

# Optionally change Grafana from a fresh-install password to the one in .env.
# A brand-new Grafana typically starts with the username and password "admin".
# This never prints the new password.
if [ -n "${GRAFANA_INITIAL_PASSWORD:-}" ]; then
    echo "🔐 Updating Grafana password from GRAFANA_INITIAL_PASSWORD..."
    BODY="$(GRAFANA_INITIAL_PASSWORD="$GRAFANA_INITIAL_PASSWORD" GRAFANA_ADMIN_PASSWORD="$GRAFANA_ADMIN_PASSWORD" python3 -c 'import json,os; print(json.dumps({"oldPassword": os.environ["GRAFANA_INITIAL_PASSWORD"], "newPassword": os.environ["GRAFANA_ADMIN_PASSWORD"]}))')"
    if curl -s -X PUT "$GRAFANA_URL/api/user/password" \
        -H "Content-Type: application/json" \
        -d "$BODY" \
        --user "$GRAFANA_USER:$GRAFANA_INITIAL_PASSWORD" > /dev/null; then
        echo "✅ Password updated to the value of GRAFANA_ADMIN_PASSWORD in your .env"
    else
        echo "⚠️  Password update failed; will try GRAFANA_ADMIN_PASSWORD as it stands"
    fi
fi

GRAFANA_PASS="$GRAFANA_ADMIN_PASSWORD"

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
echo "🌐 Grafana URL: $GRAFANA_URL"
echo "👤 Username: $GRAFANA_USER"
echo "🔑 Password: the value of GRAFANA_ADMIN_PASSWORD in your .env"
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
