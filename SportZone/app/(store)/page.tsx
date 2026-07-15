"use client";

import { useEffect, useState } from 'react';
// import { supabase } from '@/lib/supabase';
import Navbar from '@/components/store/Navbar';
import CategoryCard from '@/components/store/CategoryCard';
import ProductCard from '@/components/store/ProductCard';
import Footer from '@/components/store/Footer';

interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
  image_url: string;
}

interface Product {
  id: number;
  name: string;
  slug: string;
  description: string;
  price: number;
  mrp: number;
  images: string[];
  is_featured: boolean;
  stock_quantity: number;
}

const HomePage = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [featuredProducts, setFeaturedProducts] = useState<Product[]>([]);

  useEffect(() => {
    // Mock data for categories
    const mockCategories = [
      {
        id: 1,
        name: 'Cricket',
        slug: 'cricket',
        description: 'All cricket equipment including bats, balls, and protective gear.',
        image_url: 'https://images.unsplash.com/photo-1531415074968-036ba1b575da?w=400&h=300&fit=crop'
      },
      {
        id: 2,
        name: 'Football',
        slug: 'football',
        description: 'Football gear including balls, shoes, and accessories.',
        image_url: 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=400&h=300&fit=crop'
      },
      {
        id: 3,
        name: 'Fitness',
        slug: 'fitness',
        description: 'Fitness equipment for workouts and training.',
        image_url: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop'
      },
      {
        id: 4,
        name: 'Badminton',
        slug: 'badminton',
        description: 'Badminton rackets, shuttlecocks, and accessories.',
        image_url: 'https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=400&h=300&fit=crop'
      },
      {
        id: 5,
        name: 'Running',
        slug: 'running',
        description: 'Running shoes and gear for all levels.',
        image_url: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop'
      }
    ];

    // Mock data for featured products
    const mockFeaturedProducts = [
      {
        id: 1,
        name: 'SG Scorer Classic Bat',
        slug: 'sg-scorer-classic-bat',
        description: 'A classic cricket bat for professional players.',
        price: 2499,
        mrp: 2999,
        images: ['https://images.unsplash.com/photo-1587174486073-ae18752afe6c?w=400&h=300&fit=crop'],
        is_featured: true,
        stock_quantity: 42
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
        stock_quantity: 30
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
        stock_quantity: 18
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
        stock_quantity: 25
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
        stock_quantity: 15
      }
    ];

    setCategories(mockCategories);
    setFeaturedProducts(mockFeaturedProducts);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="hero-banner bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold mb-4">Welcome to SportZone</h1>
          <p className="text-xl">Your one-stop shop for all sports equipment!</p>
        </div>
      </div>
      <div className="categories-section max-w-7xl mx-auto py-12 px-4">
        <h2 className="text-3xl font-bold text-center mb-8">Shop by Category</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6">
          {categories.map((category) => (
            <CategoryCard key={category.id} category={category} />
          ))}
        </div>
      </div>
      <div className="featured-products-section max-w-7xl mx-auto py-12 px-4">
        <h2 className="text-3xl font-bold text-center mb-8">Featured Products</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {featuredProducts.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default HomePage;