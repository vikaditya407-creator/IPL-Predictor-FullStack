/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    domains: ['your-supabase-storage-url.com', 'images.unsplash.com'], // Replace with your Supabase storage URL
  },
};

module.exports = nextConfig;