# Troubleshooting 404 Errors

## Common Causes and Solutions

### 1. API Routes Returning 404
http://localhost:3000/api/health
**Check if API routes are accessible:**
- Visit: `` (should return JSON)
- If this works, the API routes are configured correctly

**Common issues:**
- API routes must be in `app/api/[route-name]/route.ts`
- Must export `GET`, `POST`, etc. functions
- Check server logs for errors

### 2. Component Import Errors

**If you see module not found errors:**
- Check that components are in the `components/` directory
- Verify imports use relative paths: `../components/ComponentName`
- Or use path alias: `@/components/ComponentName` (if configured)

### 3. Build Errors

**Run build to check for errors:**
```bash
npm run build
```

**Common build issues:**
- Missing dependencies: `npm install`
- TypeScript errors: Check `tsconfig.json`
- Missing files: Verify all components exist

### 4. Deployment Issues (Lovable/Vercel)

**Check deployment logs:**
- Look for build errors in deployment logs
- Verify `package.json` has correct scripts
- Check that `next.config.js` is valid

**Common deployment issues:**
- Missing environment variables
- Build timeout (increase in settings)
- Node version mismatch

### 5. Runtime Errors

**Check browser console:**
- Open DevTools (F12)
- Look for JavaScript errors
- Check Network tab for failed requests

**Check server logs:**
```bash
npm run dev
# Look for errors in terminal
```

## Quick Fixes

### Reset Everything:
```bash
# Clean install
rm -rf node_modules .next
npm install
npm run build
npm run dev
```

### Test API Routes:
```bash
# Test health endpoint
curl http://localhost:3000/api/health

# Should return: {"status":"ok","message":"API is working",...}
```

### Verify File Structure:
```
print-shop/
├── app/
│   ├── api/
│   │   ├── check-image/
│   │   │   └── route.ts
│   │   ├── batch-check/
│   │   │   └── route.ts
│   │   └── convert-heic/
│   │       └── route.ts
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── components/
│   ├── ImageUploader.tsx
│   ├── BatchProcessor.tsx
│   └── HEICConverter.tsx
└── package.json
```

## Still Having Issues?

1. **Check the exact URL causing 404:**
   - Is it the homepage `/`?
   - Is it an API route `/api/...`?
   - Is it a specific page?

2. **Check server status:**
   - Is the dev server running? (`npm run dev`)
   - Is the production build working? (`npm run build && npm start`)

3. **Check browser:**
   - Try incognito mode
   - Clear cache
   - Check Network tab for actual error

4. **Check deployment platform:**
   - Lovable/Vercel logs
   - Build status
   - Environment variables



