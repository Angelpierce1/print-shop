# Testing Your API URL

## Your Vercel URL:
```
https://print-shop-4gl6-kl59a2c42-angelpierce1s-projects.vercel.app/api/index
```

## What You Should See:

If the API is working, you should get a JSON response like:
```json
{
  "success": true,
  "message": "Print Shop AI Order Guardrail API is working!",
  "endpoints": {
    "upload": "/upload",
    "submit_order": "/submit-order",
    "validate_order": "/validate-order"
  }
}
```

## Test Commands:

### 1. Test the main endpoint:
```bash
curl https://print-shop-4gl6-kl59a2c42-angelpierce1s-projects.vercel.app/api/index
```

### 2. Test the status endpoint:
```bash
curl https://print-shop-4gl6-kl59a2c42-angelpierce1s-projects.vercel.app/api/index/status
```

### 3. Test in browser:
Just paste this URL in your browser:
```
https://print-shop-4gl6-kl59a2c42-angelpierce1s-projects.vercel.app/api/index
```

## If You Get 404:

1. **Check Vercel Dashboard:**
   - Go to your project
   - Click "Deployments"
   - Make sure latest deployment shows "Ready" (green checkmark)
   - Wait 1-2 minutes after code push for deployment to complete

2. **Check Functions Tab:**
   - In Vercel dashboard → Your project
   - Click "Functions" tab
   - Look for `api/index` in the list
   - Click on it to see logs/errors

3. **Check Build Logs:**
   - In deployment details
   - Look for any build errors
   - Check if dependencies installed correctly

## If You Get 500 Error:

Check the Function logs in Vercel dashboard - there might be:
- Import errors
- Missing dependencies
- Runtime errors

## Expected Response:

When working correctly, you should see JSON, not HTML or 404.

