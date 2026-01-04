#!/bin/bash

# SustainNet Website Observability Setup Script
# This script helps set up Grafana Cloud with AWS CloudWatch integration

set -e

echo "🚀 Setting up SustainNet Website Observability Dashboard"
echo "======================================================"

# Check if required tools are installed
command -v aws >/dev/null 2>&1 || { echo "❌ AWS CLI is required but not installed. Please install it first."; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "❌ jq is required but not installed. Please install it first."; exit 1; }

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check AWS configuration
print_status "Checking AWS configuration..."
if ! aws sts get-caller-identity >/dev/null 2>&1; then
    print_error "AWS CLI is not configured. Please run 'aws configure' first."
    exit 1
fi

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=$(aws configure get region)
print_success "AWS configured for account: $AWS_ACCOUNT_ID in region: $AWS_REGION"

# Create IAM role for Grafana CloudWatch access
print_status "Creating IAM role for Grafana CloudWatch integration..."

ROLE_NAME="grafana-cloudwatch-integration"
POLICY_NAME="grafana-cloudwatch-policy"

# Create the trust policy for Grafana Cloud
TRUST_POLICY=$(cat <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::${AWS_ACCOUNT_ID}:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "aws:PrincipalArn": "arn:aws:iam::${AWS_ACCOUNT_ID}:role/grafana-cloudwatch-integration"
        }
      }
    }
  ]
}
EOF
)

# Create the IAM policy
POLICY_DOCUMENT=$(cat <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "cloudwatch:GetMetricData",
                "cloudwatch:GetMetricStatistics",
                "cloudwatch:ListMetrics",
                "cloudfront:GetDistribution",
                "cloudfront:ListDistributions",
                "s3:GetBucketMetricsConfiguration",
                "s3:ListBucket",
                "s3:GetBucketLocation"
            ],
            "Resource": "*"
        }
    ]
}
EOF
)

# Create the policy
print_status "Creating IAM policy..."
aws iam create-policy \
    --policy-name $POLICY_NAME \
    --policy-document "$POLICY_DOCUMENT" \
    --description "Policy for Grafana CloudWatch integration" \
    >/dev/null 2>&1 || print_warning "Policy may already exist"

# Get the policy ARN
POLICY_ARN=$(aws iam list-policies --query "Policies[?PolicyName=='$POLICY_NAME'].Arn" --output text)

# Create the role
print_status "Creating IAM role..."
aws iam create-role \
    --role-name $ROLE_NAME \
    --assume-role-policy-document "$TRUST_POLICY" \
    --description "Role for Grafana to access CloudWatch metrics" \
    >/dev/null 2>&1 || print_warning "Role may already exist"

# Attach the policy to the role
print_status "Attaching policy to role..."
aws iam attach-role-policy \
    --role-name $ROLE_NAME \
    --policy-arn $POLICY_ARN

# Get the role ARN
ROLE_ARN=$(aws iam get-role --role-name $ROLE_NAME --query Role.Arn --output text)

print_success "IAM role created: $ROLE_ARN"

# Generate setup instructions
echo ""
echo "🎯 Setup Instructions"
echo "===================="
echo ""
echo "1. 🌐 Create Grafana Cloud Account:"
echo "   Visit: https://grafana.com/auth/sign-up/create-user"
echo "   Choose the free plan (3 users, 10k metrics)"
echo ""
echo "2. 🔗 Add AWS CloudWatch Data Source:"
echo "   - Go to Configuration → Data Sources → Add data source"
echo "   - Search for 'CloudWatch' and select it"
echo "   - Configure with:"
echo "     * Authentication Provider: ARN of IAM Role"
echo "     * IAM Role ARN: $ROLE_ARN"
echo "     * Default Region: $AWS_REGION"
echo ""
echo "3. 📊 Import Dashboards:"
echo "   - Go to Dashboards → Import"
echo "   - Upload the JSON files from the monitoring/ directory:"
echo "     * executive-summary-dashboard.json"
echo "     * infrastructure-dashboard.json"
echo "     * ci-cd-dashboard.json"
echo ""
echo "4. 🔐 Add to GitHub Secrets (for CI/CD monitoring):"
echo "   - GRAFANA_API_KEY: Your Grafana API key"
echo "   - GRAFANA_CLOUD_PROM_URL: Your Prometheus endpoint"
echo ""
echo "5. 📱 Access Your Dashboard:"
echo "   - Executive Summary: Business metrics and health status"
echo "   - Infrastructure: Technical performance and errors"
echo "   - CI/CD Pipeline: Deployment status and build metrics"
echo ""

print_success "Setup script completed! Follow the instructions above to complete the dashboard setup."