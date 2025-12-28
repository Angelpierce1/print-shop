# GitHub Deployment Guide

Your Print Shop application is now set up with GitHub Actions for automated CI/CD and deployment.

## What's Been Set Up

✅ **GitHub Actions Workflows:**
- **CI Workflow** (`.github/workflows/ci.yml`): Runs tests, linting, and builds on every push and pull request
- **Deploy Workflow** (`.github/workflows/deploy.yml`): Automatically deploys to Vercel when code is pushed to `main`

## Current Status

- ✅ Repository connected to: `https://github.com/Angelpierce1/print-shop.git`
- ✅ GitHub Actions workflows created and pushed
- ✅ Code is up to date on GitHub

## Next Steps for Deployment

### Option 1: Deploy to Vercel (Recommended for Next.js)

1. **Get Vercel Token:**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Navigate to Settings → Tokens
   - Create a new token

2. **Add Secret to GitHub:**
   - Go to your GitHub repository: `https://github.com/Angelpierce1/print-shop`
   - Navigate to Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `VERCEL_TOKEN`
   - Value: Your Vercel token
   - Click "Add secret"

3. **Deploy:**
   - The workflow will automatically deploy when you push to `main`
   - Or manually trigger it from the Actions tab → "Deploy to Production" → "Run workflow"

### Option 2: Deploy to GitHub Pages

If you prefer GitHub Pages, you'll need to:

1. **Update `next.config.js`** to enable static export:
   ```js
   const nextConfig = {
     output: 'export',
     reactStrictMode: true,
   }
   ```

2. **Create a GitHub Pages workflow** (or modify the existing one)

3. **Enable GitHub Pages** in repository settings:
   - Go to Settings → Pages
   - Select source: "GitHub Actions"

### Option 3: Manual Deployment

You can also deploy manually using:

```bash
# Build the app
npm run build

# Deploy to Vercel (if you have Vercel CLI installed)
vercel --prod
```

## Monitoring Deployments

- View workflow runs: `https://github.com/Angelpierce1/print-shop/actions`
- Check deployment status in the Actions tab
- View logs for any failed deployments

## Troubleshooting

- **Build fails**: Check the Actions tab for error logs
- **Vercel deployment fails**: Ensure `VERCEL_TOKEN` secret is set correctly
- **Linting errors**: Fix them locally with `npm run lint`

## Continuous Integration

Every push and pull request will:
- ✅ Run the linter
- ✅ Build the application
- ✅ Verify everything works

Every push to `main` will additionally:
- 🚀 Deploy to production (Vercel)

