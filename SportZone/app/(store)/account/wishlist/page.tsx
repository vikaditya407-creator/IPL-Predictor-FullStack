"use client";

import Link from 'next/link';
import Navbar from '@/components/store/Navbar';
import ProductCard from '@/components/store/ProductCard';
import Footer from '@/components/store/Footer';

const WishlistPage = () => {
  // Mock wishlist data
  const mockWishlist = [
    {
      id: 3,
      name: 'Yonex Nanoray 7000I Racket',
      slug: 'yonex-nanoray-7000i-racket',
      description: 'Lightweight badminton racket for quick swings.',
      price: 3199,
      mrp: 3800,
      images: ['https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=400&h=300&fit=crop'],
      is_featured: true,
      stock_quantity: 18
    },
    {
      id: 5,
      name: 'Asics Gel-Nimbus 25 Shoes',
      slug: 'asics-gel-nimbus-25-shoes',
      description: 'Comfortable running shoes for long distances.',
      price: 7499,
      mrp: 8999,
      images: ['https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop'],
      is_featured: true,
      stock_quantity: 11
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-4xl mx-auto py-16 px-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">My Wishlist</h1>

        {mockWishlist.length === 0 ? (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">❤️</div>
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">Your wishlist is empty</h2>
            <p className="text-gray-600 mb-6">Add items you love to your wishlist.</p>
            <Link
              href="/"
              className="inline-block bg-[#D85A30] text-white px-8 py-3 rounded-lg font-semibold hover:bg-[#B84525] transition-colors"
            >
              Browse Products
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockWishlist.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </div>
      <Footer />
    </div>
  );
};

export default WishlistPage;