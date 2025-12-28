/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: [],
    unoptimized: process.env.NODE_ENV === 'production' && process.env.GITHUB_PAGES === 'true',
  },
  // Enable static export for GitHub Pages
  ...(process.env.GITHUB_PAGES === 'true' && {
    output: 'export',
    trailingSlash: true,
    // Note: API routes will not work with static export
    // If you need API routes, use Vercel or another platform
  }),
}

module.exports = nextConfig




