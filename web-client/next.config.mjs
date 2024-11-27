/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: [
      "letsenhance.io",
      "t3.ftcdn.net",
      "d2sabl064492ta.cloudfront.net",
    ], // Add the required domain for images
  },
  async headers() {
    return [
      {
        source: "/(.*)", // Matches all routes
        headers: [
          { key: "Cross-Origin-Opener-Policy", value: "same-origin" },
          { key: "Cross-Origin-Resource-Policy", value: "same-origin" },
        ],
      },
    ];
  },
};

export default nextConfig;
