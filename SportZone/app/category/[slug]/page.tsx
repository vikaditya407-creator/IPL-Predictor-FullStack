"use client";

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import Navbar from '@/components/store/Navbar';
import ProductCard from '@/components/store/ProductCard';
import Footer from '@/components/store/Footer';

const CategoryPage = () => {
  const params = useParams();
  const slug = params.slug as string;
  const [category, setCategory] = useState<{
    id: number;
    name: string;
    slug: string;
    description: string;
    image_url: string;
  } | null>(null);
  const [products, setProducts] = useState<{
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
  }[]>([]);

  // Mock data
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

  const mockProducts = [
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
    },
    // Additional products for each category
    {
      id: 7,
      name: 'Kookaburra Cricket Ball',
      slug: 'kookaburra-cricket-ball',
      description: 'Professional cricket ball for matches.',
      price: 899,
      mrp: 999,
      images: ['https://images.unsplash.com/photo-1531415074968-036ba1b575da?w=400&h=300&fit=crop'],
      is_featured: false,
      stock_quantity: 50,
      category_id: 1
    },
    {
      id: 8,
      name: 'Puma Football Gloves',
      slug: 'puma-football-gloves',
      description: 'Protective gloves for goalkeepers.',
      price: 1599,
      mrp: 1799,
      images: ['https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=400&h=300&fit=crop'],
      is_featured: false,
      stock_quantity: 20,
      category_id: 2
    }
  ];

  useEffect(() => {
    const foundCategory = mockCategories.find(c => c.slug === slug);
    setCategory(foundCategory || null);

    if (foundCategory) {
      const categoryProducts = mockProducts.filter(p => p.category_id === foundCategory.id);
      setProducts(categoryProducts);
    }
  }, [slug]);

  if (!category) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex justify-center items-center h-64">
          <p className="text-xl">Category not found</p>
        </div>
        <Footer />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-7xl mx-auto py-8 px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">{category.name}</h1>
          <p className="text-gray-600 mt-2">{category.description}</p>
        </div>

        {products.length === 0 ? (
          <div className="text-center py-16">
            <p className="text-xl text-gray-600">No products found in this category.</p>
            <Link
              href="/"
              className="inline-block mt-4 bg-[#D85A30] text-white px-6 py-2 rounded-lg hover:bg-[#B84525] transition-colors"
            >
              Back to Home
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </div>
      <Footer />
    </div>
  );
};

export default CategoryPage;