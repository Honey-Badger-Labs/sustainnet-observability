#!/bin/bash

# Family Meal Planner - Local Observability Setup
# This script sets up a local Grafana + Prometheus stack for development

set -e

echo "🔧 Setting up Family Meal Planner local observability..."

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is required but not installed."
    echo "Please install Docker Desktop: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Create local observability directory structure
mkdir -p local-observability/{prometheus,grafana/dashboards,grafana/provisioning}

# Create Prometheus configuration
cat > local-observability/prometheus/prometheus.yml <<EOF
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  # FMP API metrics
  - job_name: 'family-meal-planner-api'
    static_configs:
      - targets: ['fmp-api:3001']
    metrics_path: '/metrics'

  # Redis metrics (if exporter is added)
  - job_name: 'family-meal-planner-cache'
    static_configs:
      - targets: ['redis-exporter:9121']

  # PostgreSQL metrics (if exporter is added)
  - job_name: 'family-meal-planner-db'
    static_configs:
      - targets: ['postgres-exporter:9187']
EOF

# Create Grafana provisioning config for dashboards
cat > local-observability/grafana/provisioning/dashboards.yml <<EOF
apiVersion: 1

providers:
  - name: 'FMP Dashboards'
    orgId: 1
    folder: 'Family Meal Planner'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 10
    options:
      path: /etc/grafana/dashboards
EOF

# Create Grafana provisioning config for datasources
cat > local-observability/grafana/provisioning/datasources.yml <<EOF
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
EOF

# Copy dashboards to Grafana directory
cp api-performance-dashboard.json local-observability/grafana/dashboards/
cp user-engagement-dashboard.json local-observability/grafana/dashboards/
cp mobile-app-health-dashboard.json local-observability/grafana/dashboards/

# Create docker-compose for observability stack
cat > local-observability/docker-compose.yml <<EOF
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: fmp-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    networks:
      - fmp-observability

  grafana:
    image: grafana/grafana:latest
    container_name: fmp-grafana
    ports:
      - "3002:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana_data:/var/lib/grafana
      - ./grafana/dashboards:/etc/grafana/dashboards
      - ./grafana/provisioning:/etc/grafana/provisioning
    depends_on:
      - prometheus
    networks:
      - fmp-observability

  redis-exporter:
    image: oliver006/redis_exporter:latest
    container_name: fmp-redis-exporter
    ports:
      - "9121:9121"
    environment:
      - REDIS_ADDR=redis:6379
    networks:
      - fmp-observability

  postgres-exporter:
    image: prometheuscommunity/postgres-exporter:latest
    container_name: fmp-postgres-exporter
    ports:
      - "9187:9187"
    environment:
      - DATA_SOURCE_NAME=postgresql://sustainnet:localdev123@postgres:5432/sustainnet_local?sslmode=disable
    networks:
      - fmp-observability

networks:
  fmp-observability:
    external: true
    name: sustainnet-network  # Connect to existing local dev network

volumes:
  prometheus_data:
  grafana_data:
EOF

echo "✅ Observability configuration created"

# Start observability stack
echo "🚀 Starting Prometheus + Grafana..."
cd local-observability
docker-compose up -d

echo ""
echo "✅ Family Meal Planner observability stack is running!"
echo ""
echo "📊 Access points:"
echo "   Grafana:    http://localhost:3000 (admin/admin)"
echo "   Prometheus: http://localhost:9090"
echo ""
echo "📈 Dashboards available in Grafana:"
echo "   - API Performance"
echo "   - User Engagement"
echo "   - Mobile App Health"
echo ""
echo "⚠️  Note: Metrics collection requires instrumentation in the FMP API"
echo "   See README.md for instrumentation guide"
