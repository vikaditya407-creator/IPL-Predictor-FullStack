# SportZone

SportZone is a production-ready e-commerce website for sports equipment built using Next.js, TypeScript, and Tailwind CSS. The platform allows users to browse, search, and purchase a variety of sports products, while also providing an admin panel for managing products, orders, and categories.

## Features

- **User Authentication**: Secure login and registration with Supabase Auth, including Google OAuth.
- **Product Browsing**: Users can view products by category, search for specific items, and filter results.
- **Shopping Cart**: Users can add items to their cart, adjust quantities, and proceed to checkout.
- **Checkout Process**: Supports multiple payment options, including Razorpay and Cash on Delivery.
- **Order Management**: Users can view their past orders and track their status.
- **Wishlist**: Users can save products for later purchase.
- **Admin Panel**: Admin users can manage products, categories, and orders efficiently.

## Tech Stack

- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS
- **Backend**: Supabase (PostgreSQL, Auth, Storage)
- **Payments**: Razorpay
- **Deployment**: Vercel

## Database Schema

The application uses the following database tables:

- **categories**: Stores product categories.
- **products**: Contains product details.
- **orders**: Manages user orders.
- **cart_items**: Tracks items in user carts.
- **wishlist**: Saves user wishlist items.
- **admin_users**: Manages admin access.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd SportZone
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory and add the following variables:
   ```
   NEXT_PUBLIC_SUPABASE_URL=<your-supabase-url>
   NEXT_PUBLIC_SUPABASE_ANON_KEY=<your-supabase-anon-key>
   SUPABASE_SERVICE_ROLE_KEY=<your-supabase-service-role-key>
   NEXT_PUBLIC_RAZORPAY_KEY_ID=<your-razorpay-key-id>
   RAZORPAY_KEY_SECRET=<your-razorpay-key-secret>
   NEXT_PUBLIC_SITE_URL=<your-site-url>
   ```

4. Run the development server:
   ```
   npm run dev
   ```

5. Open your browser and navigate to `http://localhost:3000`.

## Usage

- Visit the homepage to explore featured products and categories.
- Use the search bar to find specific items.
- Add products to your cart and proceed to checkout.
- Admin users can access the admin panel to manage products and orders.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.