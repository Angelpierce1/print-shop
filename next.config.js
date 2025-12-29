/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    // This prevents Webpack from trying to bundle the rust binary
    serverComponentsExternalPackages: ["@napi-rs/canvas"],
  },
  webpack: (config, { isServer }) => {
    if (isServer) {
      // Externalize @napi-rs/canvas for server-side rendering
      config.externals = config.externals || []
      config.externals.push({
        '@napi-rs/canvas': 'commonjs @napi-rs/canvas',
      })
    }
    return config
  },
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




