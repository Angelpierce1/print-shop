# How to Test Your Deployment

## ⚠️ Important: Use Default Vercel Domain First

**DO NOT use `www.timsprintshop.com` yet** - it's not configured. Use your default Vercel domain instead.

## Step 1: Find Your Vercel URL

1. Go to [vercel.com](https://vercel.com) and **sign in**
2. Click on your project (**print-shop**)
3. Look at the **top of the page** - you'll see your deployment URL
4. It will look like: `https://print-shop-xxxxx.vercel.app`

**This is the URL you should use for testing!**

## Step 2: Test Your API Endpoints

Replace `your-project-name` with your actual Vercel project name:

### Test Root Endpoint:
```
https://your-project-name.vercel.app/api/index
```

Or in your browser, just visit:
```
https://your-project-name.vercel.app/api
```

### Test Upload Endpoint (using curl):
```bash
curl -X POST https://your-project-name.vercel.app/api/upload \
  -F "file=@your-image.jpg"
```

### Test Submit Order Endpoint:
```bash
curl -X POST https://your-project-name.vercel.app/api/submit-order \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "size": "8.5x11",
    "paper": "100lb Matte",
    "quantity": 100,
    "filename": "test.jpg"
  }'
```

## Step 3: Check Deployment Status

In Vercel Dashboard:
1. Go to **Deployments** tab
2. Check if the latest deployment is **Ready** (green checkmark)
3. Click on the deployment to see logs
4. Check **Functions** tab to see if `api/index` is listed

## Common Issues:

### If you get 404:
- Make sure you're using `/api/index` not just `/api`
- Check that deployment completed successfully
- Verify function is listed in Functions tab

### If you get 500 error:
- Check Function logs in Vercel dashboard
- Look for import errors or missing dependencies
- Verify all dependencies are in `requirements.txt`

### If deployment is failing:
- Check build logs in Vercel dashboard
- Verify `requirements.txt` has all dependencies
- Make sure Python version is compatible

## After Testing Works:

Once your API works on the default `.vercel.app` domain, you can:
1. Set up custom domain `www.timsprintshop.com` in Vercel dashboard
2. Configure DNS at your domain registrar
3. Wait for DNS propagation

**But first, make sure everything works on the default domain!**

