# Deploying to Vercel

Your code has been pushed to GitHub. To deploy to Vercel, choose one of these methods:

## Method 1: GitHub Integration (Recommended)

1. **Go to [vercel.com](https://vercel.com)** and sign in
2. **Click "Add New Project"**
3. **Import your GitHub repository**: `Angelpierce1/print-shop`
4. **Vercel will auto-detect**:
   - Framework: Python (Serverless Functions)
   - Root Directory: `.` (root)
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
5. **Click "Deploy"**

Vercel will automatically deploy your API and provide a URL like:
`https://your-project.vercel.app/api`

## Method 2: Vercel CLI

1. **Install Vercel CLI** (if not installed):
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

   For production deployment:
   ```bash
   vercel --prod
   ```

## API Endpoints

Once deployed, your API will be available at:

- **Base URL**: `https://your-project.vercel.app/api`

### Available Actions:

1. **Info** (GET):
   ```
   GET https://your-project.vercel.app/api
   ```

2. **Process Order** (POST):
   ```json
   POST https://your-project.vercel.app/api
   {
     "action": "process_order",
     "query": "I need 500 business cards",
     "file_path": "optional-file-path"
   }
   ```

3. **Check Inventory** (POST):
   ```json
   POST https://your-project.vercel.app/api
   {
     "action": "check_inventory",
     "paper_stock": "100lb_cardstock",
     "color": "white",
     "finish": "matte"
   }
   ```

4. **Calculate Price** (POST):
   ```json
   POST https://your-project.vercel.app/api
   {
     "action": "calculate_price",
     "paper_stock": "100lb_cardstock",
     "quantity": 500,
     "width_inches": 3.5,
     "height_inches": 2.0,
     "full_color": true
   }
   ```

5. **Test Guardrails** (POST):
   ```json
   POST https://your-project.vercel.app/api
   {
     "action": "test_guardrails"
   }
   ```

## Testing the Deployment

After deployment, test your API:

```bash
curl https://your-project.vercel.app/api
```

Or test with a specific action:

```bash
curl -X POST https://your-project.vercel.app/api \
  -H "Content-Type: application/json" \
  -d '{"action": "test_guardrails"}'
```

## Notes

- **File Uploads**: The current implementation expects file paths. For production, you'll want to handle file uploads via base64 or URL.
- **Environment Variables**: If you add LLM integration later, add API keys in Vercel's Environment Variables settings.
- **Cold Starts**: Python serverless functions may have cold start delays (~1-2 seconds).

## Troubleshooting

- Check Vercel dashboard logs if deployment fails
- Ensure `requirements.txt` includes all dependencies
- Python version is automatically detected (Python 3.9+)

