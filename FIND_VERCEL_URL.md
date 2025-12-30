# How to Find Your Vercel Deployment URL

## Method 1: Vercel Dashboard (Easiest)

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click on your project (likely named `print-shop`)
3. Look at the top of the page - you'll see your deployment URL
4. It will look like: `https://print-shop-xxxxx.vercel.app`

## Method 2: Check Deployment History

1. In Vercel dashboard → Your project
2. Go to "Deployments" tab
3. Click on the latest deployment
4. The URL is shown at the top

## Method 3: Using Vercel CLI

```bash
# Install Vercel CLI (if not installed)
npm install -g vercel

# Login
vercel login

# List your projects
vercel ls

# Or get project info
vercel inspect
```

## Your API Endpoints

Once you have your Vercel URL (let's say it's `https://print-shop-abc123.vercel.app`):

### Main API Endpoint:
```
https://print-shop-abc123.vercel.app/api/index
```

### Test Endpoint:
```
https://print-shop-abc123.vercel.app/api/test
```

## Testing Your API

Once you have the URL, test it:

```bash
# Replace with your actual URL
curl https://your-project.vercel.app/api/index
```

Or in a browser, just visit:
```
https://your-project.vercel.app/api/index
```

## If You Haven't Deployed Yet

If you don't see a project in Vercel:

1. Go to [vercel.com](https://vercel.com)
2. Click "Add New Project"
3. Import from GitHub: `Angelpierce1/print-shop`
4. Click "Deploy"
5. Wait for deployment to complete
6. Copy the URL shown

## Quick Test

The simplest way is to:
1. Open Vercel dashboard
2. Find your project
3. Copy the URL shown
4. Add `/api/index` to the end
5. Test in browser or with curl

