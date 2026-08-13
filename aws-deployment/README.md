# AWS Deployment Configuration for AI Career Agent

This directory contains files for deploying to AWS using ECS (Elastic Container Service) and other AWS services.

## Architecture

- **AWS ECR**: Docker image repository
- **AWS ECS**: Container orchestration
- **AWS RDS**: PostgreSQL database
- **AWS ElastiCache**: Redis cache
- **AWS ALB**: Application Load Balancer
- **AWS CloudFormation/CDK**: Infrastructure as Code

## Files in this directory:

1. `ecs-task-definition.json` - ECS task configuration
2. `deploy.sh` - Deployment automation script
3. `cloudformation-template.yaml` - Infrastructure as Code template

## Prerequisites

- AWS CLI configured: `aws configure`
- Docker installed and running
- AWS Account with appropriate permissions
- ECR repositories created

## Quick Setup

```bash
# 1. Set AWS region
export AWS_REGION=us-east-1
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# 2. Create ECR repositories
aws ecr create-repository --repository-name ai-career-agent-backend
aws ecr create-repository --repository-name ai-career-agent-frontend
aws ecr create-repository --repository-name ai-career-agent-worker

# 3. Build and push images
./deploy.sh build-and-push

# 4. Deploy to ECS
./deploy.sh deploy-ecs
```

See individual files for detailed instructions.
