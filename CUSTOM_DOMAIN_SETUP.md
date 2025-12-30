# Setting Up Custom Domain: timsprintshop.com

## Current Issue
The domain `www.timsprintshop.com` is not yet configured. You need to:
1. Deploy to Vercel first (to get a working app)
2. Add the custom domain in Vercel
3. Configure DNS records

## Step-by-Step Setup

### Step 1: Deploy to Vercel (if not already deployed)

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "Add New Project"
3. Import repository: `Angelpierce1/print-shop`
4. Click "Deploy"
5. Wait for deployment to complete

You'll get a default domain like: `print-shop-xxxxx.vercel.app`

**Test this first** to make sure your app works!

### Step 2: Add Custom Domain in Vercel

1. In your Vercel project dashboard, go to **Settings** → **Domains**
2. Click **Add Domain**
3. Enter your domain:
   - For www: `www.timsprintshop.com`
   - For root domain: `timsprintshop.com` (recommended to add both)
4. Vercel will show you the DNS records you need to configure

### Step 3: Configure DNS Records

You need to add DNS records in your domain registrar (where you bought timsprintshop.com):

#### Option A: CNAME (Recommended for www subdomain)

Add these DNS records in your domain registrar:

**For www.timsprintshop.com:**
- **Type**: CNAME
- **Name**: www
- **Value**: `cname.vercel-dns.com`
- **TTL**: Auto or 3600

**For root domain (timsprintshop.com):**
- **Type**: A
- **Name**: @ (or leave blank)
- **Value**: `76.76.21.21` (Vercel's IP - check Vercel dashboard for current IP)

OR use an ANAME/ALIAS record:
- **Type**: ANAME/ALIAS (if supported by your DNS provider)
- **Name**: @
- **Value**: `cname.vercel-dns.com`

#### Option B: Using Vercel Nameservers (Easiest)

1. In Vercel dashboard, go to **Settings** → **Domains**
2. Select your domain
3. Choose **Use Vercel DNS**
4. Vercel will provide nameservers like:
   - `ns1.vercel-dns.com`
   - `ns2.vercel-dns.com`
5. Update nameservers in your domain registrar to point to Vercel's nameservers

### Step 4: Verify DNS Propagation

DNS changes can take up to 48 hours, but usually happen within minutes to hours.

Check propagation:
```bash
# Check if DNS is resolving
dig www.timsprintshop.com
# or
nslookup www.timsprintshop.com
```

Or use online tools:
- https://dnschecker.org
- https://www.whatsmydns.net

### Step 5: SSL Certificate

Vercel automatically provisions SSL certificates for your custom domain. This usually happens within a few minutes after DNS is configured correctly.

## Troubleshooting

### DNS_PROBE_FINISHED_NXDOMAIN
This error means DNS is not configured or not propagated yet.

**Solutions:**
1. Wait for DNS propagation (can take up to 48 hours)
2. Double-check DNS records match Vercel's requirements exactly
3. Verify domain is added in Vercel dashboard
4. Clear your browser DNS cache or try a different network

### Check Current Status

1. **In Vercel Dashboard**: Settings → Domains → Check if domain shows as "Valid Configuration"
2. **DNS Check**: Use dnschecker.org to see if DNS records are propagated globally
3. **Vercel Status**: Check if deployment is successful

## Quick Test Commands

After DNS is configured:

```bash
# Test if domain resolves
curl -I https://www.timsprintshop.com/api

# Test API endpoint
curl https://www.timsprintshop.com/api
```

## Important Notes

- **Domain Ownership**: You must own `timsprintshop.com` to configure it
- **DNS Provider**: The DNS configuration happens at your domain registrar (GoDaddy, Namecheap, etc.), not in the code
- **Propagation Time**: DNS changes typically take 5 minutes to 48 hours
- **Both www and root**: Consider configuring both `www.timsprintshop.com` and `timsprintshop.com` with redirects

## Need Help?

1. Check Vercel's domain documentation: https://vercel.com/docs/concepts/projects/domains
2. Verify your deployment works first on the `.vercel.app` domain
3. Check DNS records match exactly what Vercel shows

