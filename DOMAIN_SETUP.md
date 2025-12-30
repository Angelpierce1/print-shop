# Domain Setup Guide

## Current Issue: DNS Error

The error `DNS_PROBE_FINISHED_NXDOMAIN` means `www.timsprintshop.com` is not yet pointing to your Vercel deployment.

## Step 1: Use Your Default Vercel Domain First

**Before setting up a custom domain, test with Vercel's default domain:**

1. Go to [vercel.com](https://vercel.com) and sign in
2. Open your project (should be `print-shop`)
3. Look at the top of the page - you'll see your deployment URL
4. It will look like: `https://print-shop-xxxxx.vercel.app`

**Test your API with the default domain:**
```
https://your-project-name.vercel.app/api/index
```

## Step 2: Set Up Custom Domain (Optional)

Once your API works on the default domain, you can add the custom domain:

### In Vercel Dashboard:

1. Go to **Settings** → **Domains**
2. Click **Add Domain**
3. Enter: `www.timsprintshop.com`
4. Vercel will show you DNS records to add

### At Your Domain Registrar:

Wherever you bought `timsprintshop.com` (GoDaddy, Namecheap, etc.), add:

**For www.timsprintshop.com:**
- **Type**: CNAME
- **Name**: `www`
- **Value**: `cname.vercel-dns.com`
- **TTL**: Auto or 3600

**For root domain (timsprintshop.com):**
- **Type**: A
- **Name**: `@` (or leave blank)
- **Value**: `76.76.21.21` (check Vercel dashboard for current IP)

OR use Vercel's nameservers:
- Update nameservers to: `ns1.vercel-dns.com` and `ns2.vercel-dns.com`

### Wait for DNS Propagation:

- Can take 5 minutes to 48 hours
- Usually works within 1-2 hours
- Check at: https://dnschecker.org

## Important Notes:

- **DNS configuration happens at your domain registrar, NOT in your code**
- **You must own the domain** to configure it
- **Test on default Vercel domain first** before setting up custom domain
- **Custom domain is optional** - the default `.vercel.app` domain works fine

## Quick Test Commands:

```bash
# Test with default Vercel domain (replace with your actual URL)
curl https://your-project.vercel.app/api/index

# After DNS is configured, test custom domain
curl https://www.timsprintshop.com/api/index
```

