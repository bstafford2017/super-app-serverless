# super-app-serverless 🚀

Backend architecture for super-app

## [Architecture](./docs/architecture.jpg)

## Overview 📝

This project is a Python-based, serverless backend for the Super App, deployed on AWS using CloudFormation and Lambda. It includes:

- 🐍 Python Lambda functions for authentication and fact generation
- 🔐 AWS Cognito for user authentication
- 🤖 AWS Bedrock for AI/ML model inference
- 🌐 API Gateway for HTTP endpoints
- 🛡️ IAM for secure permissions
- 🗄️ S3 for Lambda deployment packages

## Key Features ✨

- 🚫 **No Node.js/Serverless Framework**: Pure Python and AWS native tools
- 🤖 **CI/CD**: Automated with GitHub Actions and AWS CLI
- 💸 **Cost Optimized**: Uses minimal Lambda resources and efficient Bedrock models
- 🔒 **Secure**: Cognito authorizer for protected endpoints

## Deployment Steps 🛠️

1. 📦 **Package Lambda code** and upload to S3
2. ☁️ **Deploy CloudFormation stacks** for S3, Lambda, IAM, Cognito, and API Gateway
3. 🤖 **Automated CI/CD** via `.github/workflows/deploy.yml`

## Directory Structure 📁

```
docs/                   # Documentation
serverless-resources/   # CloudFormation templates
src/
  handlers/             # Lambda function handlers
```

## Requirements ⚙️

- 🐍 Python 3.9+
- 🖥️ AWS CLI
- 📦 boto3

## How to Deploy 🚀

See the [GitHub Actions workflow](.github/workflows/deploy.yml) for automated deployment steps, or follow the manual steps in the project documentation.

## Authors 👤

Benjamin Stafford
