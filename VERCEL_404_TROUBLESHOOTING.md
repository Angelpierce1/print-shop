# Fixing 404 NOT_FOUND Error on Vercel

## Understanding the Error

The `404: NOT_FOUND` error means Vercel can't find the route you're trying to access.

## Correct URLs to Try

For Python serverless functions in Vercel, the route is based on the file path:

- File: `api/index.py` → URL: `/api/index` (not `/api`)
- File: `api/test.py` → URL: `/api/test`

### Try These URLs:

1. **Primary endpoint**:
   ```
   https://your-project.vercel.app/api/index
   ```

2. **Test endpoint** (simpler, to verify functions work):
   ```
   https://your-project.vercel.app/api/test
   ```

3. **With rewrite** (if configured):
   ```
   https://your-project.vercel.app/api
   ```
   (This should redirect to `/api/index`)

## Step-by-Step Troubleshooting

### 1. Verify Deployment Status

1. Go to [vercel.com](https://vercel.com) dashboard
2. Open your project
3. Check the latest deployment:
   - Is it "Ready" (green)?
   - Are there any build errors?
   - Check the "Functions" tab - do you see `api/index` listed?

### 2. Check Function Logs

1. In Vercel dashboard → Your project → Functions tab
2. Click on `api/index`
3. Check for any errors or import issues
4. Look at the "Logs" section for runtime errors

### 3. Test with Simple Endpoint

I've created `api/test.py` as a simple test. Try:
```
https://your-project.vercel.app/api/test
```

If this works but `/api/index` doesn't, there's likely an import error in `api/index.py`.

### 4. Common Issues

#### Issue: Import Errors
**Symptom**: Function shows in dashboard but returns 404 or 500

**Solution**: Check if all dependencies are in `requirements.txt`:
```bash
Pillow>=10.0.0
PyMuPDF>=1.23.0
python-dateutil>=2.8.0
```

#### Issue: Wrong URL
**Symptom**: Getting 404 on `/api` but not `/api/index`

**Solution**: Always use `/api/index` (the full path matches the file name)

#### Issue: Handler Format
**Symptom**: Function exists but doesn't respond

**Solution**: Ensure handler function signature is:
```python
def handler(req):
    return {
        "statusCode": 200,
        "headers": {...},
        "body": "..."
    }
```

### 5. Verify Your Deployment

Run these commands to test:

```bash
# Test 1: Simple test endpoint
curl https://your-project.vercel.app/api/test

# Test 2: Main endpoint
curl https://your-project.vercel.app/api/index

# Test 3: With POST request
curl -X POST https://your-project.vercel.app/api/index \
  -H "Content-Type: application/json" \
  -d '{"action": "test_guardrails"}'
```

## Quick Fix Checklist

- [ ] Deployment is successful (green status in Vercel dashboard)
- [ ] Using correct URL: `/api/index` not `/api`
- [ ] All dependencies in `requirements.txt`
- [ ] No import errors in Function logs
- [ ] Handler function is named `handler(req)`
- [ ] Test endpoint `/api/test` works (if it does, imports are fine)

## If Still Not Working

1. **Check Vercel Dashboard → Functions → api/index → Logs**
   - Look for Python import errors
   - Check for missing dependencies

2. **Redeploy**:
   - Make a small change (add a comment)
   - Commit and push
   - Vercel will redeploy automatically

3. **Simplify to test**:
   - Temporarily comment out imports in `api/index.py`
   - Return a simple JSON response
   - If that works, the issue is with imports

4. **Contact Vercel Support**:
   - Share the deployment URL
   - Share the error ID (like `sfo1::qtl5k-1767103934875-d37e027d97d9`)
   - Share function logs

## Expected Response

When working correctly, you should get:

```json
{
  "success": true,
  "message": "Print Shop AI Order Guardrail API",
  "available_actions": [...]
}
```


