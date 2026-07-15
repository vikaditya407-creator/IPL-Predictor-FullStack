"use client";

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import Navbar from '@/components/store/Navbar';
import ProductCard from '@/components/store/ProductCard';
import Footer from '@/components/store/Footer';

const SearchPage = () => {
  const searchParams = useSearchParams();
  const query = searchParams.get('q') || '';

  // Mock products data
  const mockProducts: {
    id: number;
    name: string;
    slug: string;
    description: string;
    price: number;
    mrp: number;
    images: string[];
    is_featured: boolean;
    stock_quantity: number;
    category_id: number;
  }[] = [
    {
      id: 1,
      name: 'SG Scorer Classic Bat',
      slug: 'sg-scorer-classic-bat',
      description: 'A classic cricket bat for professional players.',
      price: 2499,
      mrp: 2999,
      images: ['https://images.unsplash.com/photo-1587174486073-ae18752afe6c?w=400&h=300&fit=crop'],
      is_featured: true,
      stock_quantity: 42,
      category_id: 1
    },
    {
      id: 2,
      name: 'Nike Strike Football',
      slug: 'nike-strike-football',
      description: 'Durable football for all weather conditions.',
      price: 1299,
      mrp: 1299,
      images: ['https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=400&h=300&fit=crop'],
      is_featured: true,
      stock_quantity: 30,
      category_id: 2
    },
    {
      id: 3,
      name: 'Yonex Nanoray 7000I Racket',
      slug: 'yonex-nanoray-7000i-racket',
      description: 'Lightweight badminton racket for quick swings.',
      price: 3199,
      mrp: 3800,
      images: ['https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=400&h=300&fit=crop'],
      is_featured: true,
      stock_quantity: 18,
      category_id: 4
    },
    {
      id: 4,
      name: 'Nivia 20kg Dumbbell Set',
      slug: 'nivia-20kg-dumbbell-set',
      description: 'Adjustable dumbbell set for home workouts.',
      price: 1899,
      mrp: 1899,
      images: ['https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop'],
      is_featured: true,
      stock_quantity: 25,
      category_id: 3
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
      stock_quantity: 11,
      category_id: 5
    },
    {
      id: 6,
      name: 'Adidas Predator Football Boots',
      slug: 'adidas-predator-football-boots',
      description: 'Professional football boots with advanced grip technology.',
      price: 8999,
      mrp: 10999,
      images: ['https://images.unsplash.com/photo-1543326727-cf6c39e8f84c?w=400&h=300&fit=crop'],
      is_featured: true,
      stock_quantity: 15,
      category_id: 2
    }
  ];

  const [searchResults, setSearchResults] = useState<typeof mockProducts>([]);
  const [searchQuery, setSearchQuery] = useState(query);

  useEffect(() => {
    if (searchQuery.trim()) {
      const results = mockProducts.filter(product =>
        product.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        product.description.toLowerCase().includes(searchQuery.toLowerCase())
      );
      setSearchResults(results);
    } else {
      setSearchResults([]);
    }
  }, [searchQuery]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // Update URL with search query
    const url = new URL(window.location.href);
    url.searchParams.set('q', searchQuery);
    window.history.pushState({}, '', url.toString());
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-4xl mx-auto py-8 px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Search Products</h1>
          <form onSubmit={handleSearch} className="flex gap-2">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search for products..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              type="submit"
              className="bg-[#D85A30] text-white px-6 py-2 rounded-lg hover:bg-[#B84525] transition-colors"
            >
              Search
            </button>
          </form>
        </div>

        {searchQuery && (
          <div className="mb-6">
            <p className="text-gray-600">
              {searchResults.length} result{searchResults.length !== 1 ? 's' : ''} for "{searchQuery}"
            </p>
          </div>
        )}

        {searchResults.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {searchResults.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        ) : searchQuery ? (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">🔍</div>
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">No products found</h2>
            <p className="text-gray-600">Try searching with different keywords</p>
          </div>
        ) : (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">🛍️</div>
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">Start your search</h2>
            <p className="text-gray-600">Enter a product name or description above</p>
          </div>
        )}
      </div>
      <Footer />
    </div>
  );
};

export default SearchPage;