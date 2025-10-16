# 🚀 Tennis AI - Deployment Guide

## ⚠️ Important Note About AWS Amplify

**AWS Amplify is NOT compatible with Streamlit applications** because:
- Amplify is designed for frontend frameworks (React, Vue, Angular, Next.js)
- Streamlit requires a Python runtime and persistent server process
- Streamlit uses WebSocket connections for real-time updates

## ✅ Recommended Deployment Options

### **Option 1: AWS App Runner (RECOMMENDED)**

**Best for:** Production deployments with auto-scaling and easy management

**Advantages:**
- ✅ Easiest AWS solution for containers
- ✅ Auto-scaling built-in
- ✅ Automatic HTTPS
- ✅ Simple deployment from Docker
- ✅ Pay only for what you use

**Cost:** ~$25-50/month for low-medium traffic

#### Quick Start:

```bash
# 1. Make the deployment script executable
chmod +x deploy-apprunner.sh

# 2. Ensure your .env file has AWS credentials
cp .env.example .env
# Edit .env with your credentials

# 3. Deploy!
./deploy-apprunner.sh
```

That's it! The script will:
- Create ECR repository
- Build and push Docker image
- Create/update App Runner service
- Provide you with the live URL

#### Manual Deployment:

See [deploy-to-apprunner.md](./deploy-to-apprunner.md) for detailed manual steps.

---

### **Option 2: Streamlit Community Cloud (FREE)**

**Best for:** Public demos, MVPs, testing

**Advantages:**
- ✅ Completely FREE
- ✅ Easiest setup (no AWS needed)
- ✅ Direct GitHub integration
- ✅ Automatic deployments

**Limitations:**
- ⚠️ App must be public
- ⚠️ Limited resources
- ⚠️ Community support only

#### Quick Start:

1. Push your code to GitHub (make repository public)
2. Go to https://share.streamlit.io/
3. Sign in with GitHub
4. Click "New app"
5. Select your repository and branch
6. Set main file path: `app.py`
7. Add secrets in Streamlit Cloud dashboard:
   ```
   AWS_ACCESS_KEY_ID = "your_key"
   AWS_SECRET_ACCESS_KEY = "your_secret"
   AWS_SESSION_TOKEN = "your_token"
   ```
8. Click "Deploy"!

Your app will be live at: `https://share.streamlit.io/[username]/[repo-name]`

---

### **Option 3: AWS ECS Fargate**

**Best for:** Large-scale production with custom networking

**Advantages:**
- ✅ Maximum scalability
- ✅ Full control over infrastructure
- ✅ VPC integration
- ✅ Load balancing

**Cost:** ~$30-60/month

See [deploy-to-apprunner.md](./deploy-to-apprunner.md) for ECS deployment steps.

---

### **Option 4: AWS Elastic Beanstalk**

**Best for:** Traditional AWS deployments

**Advantages:**
- ✅ Easy Docker support
- ✅ Managed platform
- ✅ Good for existing AWS users

**Cost:** ~$20-40/month

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p docker tennis-ai-streamlit --region us-east-1

# Create environment and deploy
eb create tennis-ai-env

# Set environment variables
eb setenv AWS_ACCESS_KEY_ID=xxx AWS_SECRET_ACCESS_KEY=xxx AWS_SESSION_TOKEN=xxx

# Open app
eb open
```

---

### **Option 5: AWS EC2 (Manual)**

**Best for:** Complete control, custom configurations

**Steps:**

1. Launch EC2 instance (Ubuntu 22.04 recommended)
2. Install Docker:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```
3. Clone your repository
4. Create `.env` file with credentials
5. Run with Docker Compose:
   ```bash
   docker-compose up -d
   ```
6. Configure security group to allow port 8501
7. Access via: `http://[ec2-public-ip]:8501`

**Cost:** ~$10-30/month (t2.small - t2.medium)

---

## 🔒 Security Best Practices

### 1. Use AWS Secrets Manager (Recommended)

Instead of environment variables, store credentials in Secrets Manager:

```bash
# Create secret
aws secretsmanager create-secret \
    --name tennis-ai/aws-credentials \
    --secret-string '{
        "AWS_ACCESS_KEY_ID": "xxx",
        "AWS_SECRET_ACCESS_KEY": "xxx",
        "AWS_SESSION_TOKEN": "xxx"
    }'
```

Then update your code to fetch from Secrets Manager.

### 2. Use IAM Roles (Best Practice)

For App Runner/ECS/EC2, assign IAM roles instead of hardcoding credentials:
- Create IAM role with Bedrock and Polly permissions
- Attach to your service
- Remove AWS credentials from code

### 3. Secure Environment Variables

- Never commit `.env` to version control
- Use different credentials for dev/staging/prod
- Rotate credentials regularly

---

## 📊 Cost Comparison

| Option | Monthly Cost | Setup Difficulty | Best For |
|--------|-------------|------------------|----------|
| **Streamlit Cloud** | FREE | ⭐⭐⭐⭐⭐ Easy | Public demos, MVPs |
| **EC2 (t2.small)** | ~$10-15 | ⭐⭐⭐ Medium | Budget deployments |
| **Elastic Beanstalk** | ~$20-40 | ⭐⭐⭐⭐ Easy | AWS-familiar teams |
| **App Runner** | ~$25-50 | ⭐⭐⭐⭐⭐ Easy | Production (small/medium) |
| **ECS Fargate** | ~$30-60 | ⭐⭐ Hard | Large-scale production |

---

## 🔧 Updating Your Deployed App

### App Runner:
```bash
./deploy-apprunner.sh  # Automatically builds and deploys
```

### Streamlit Cloud:
```bash
git push origin main  # Auto-deploys on push
```

### Elastic Beanstalk:
```bash
eb deploy
```

### EC2:
```bash
ssh into-ec2
cd /path/to/app
git pull
docker-compose restart
```

---

## 📝 Monitoring & Logs

### App Runner:
```bash
# View logs
aws logs tail /aws/apprunner/tennis-ai-streamlit --follow

# Check service status
aws apprunner describe-service --service-arn YOUR_ARN
```

### Streamlit Cloud:
- View logs in Streamlit Cloud dashboard
- Real-time logs in the web interface

### Docker (Local/EC2):
```bash
docker logs tennis-ai-onboarding -f
```

---

## 🐛 Troubleshooting

### App won't start
1. Check Docker image builds locally: `docker build -t test .`
2. Test locally: `docker run -p 8501:8501 test`
3. Check environment variables are set correctly
4. Review logs for errors

### Health check failing
1. Verify Streamlit responds to `/_stcore/health`
2. Check port mapping (should be 8501)
3. Increase health check timeout in config

### AWS credentials not working
1. Verify credentials in `.env` file
2. Test AWS CLI: `aws sts get-caller-identity`
3. Check IAM permissions for Bedrock and Polly
4. Ensure credentials are not expired

### High costs
1. Use smaller instance sizes
2. Enable auto-scaling with min instances = 0
3. Consider Streamlit Cloud for non-production
4. Use spot instances on EC2

---

## 📚 Additional Resources

- [AWS App Runner Documentation](https://docs.aws.amazon.com/apprunner/)
- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [Streamlit Deployment Guide](https://docs.streamlit.io/knowledge-base/tutorials/deploy)

---

## 🆘 Need Help?

1. Check logs first
2. Review AWS service health status
3. Verify all credentials and permissions
4. Test Docker image locally
5. Check security groups and network settings

---

## 📈 Recommended Path

1. **Development**: Run locally with Docker
2. **Testing**: Deploy to Streamlit Cloud (free)
3. **Staging**: Deploy to App Runner (small instance)
4. **Production**: App Runner or ECS Fargate with proper monitoring

---

**Last Updated:** October 2025

