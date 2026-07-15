"use client";

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { supabase } from '@/lib/supabase';
import ProductCard from '@/components/store/ProductCard';
import { Category, Product } from '@/types';

const CategoryPage = () => {
  const params = useParams();
  const slug = params?.slug as string | undefined;
  const [category, setCategory] = useState<Category | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) return;

    const fetchCategoryAndProducts = async () => {
      setLoading(true);
      setErrorMessage(null);

      try {
        const { data: categoryData, error: categoryError } = await supabase
          .from('categories')
          .select('*')
          .eq('slug', slug)
          .single();

        if (categoryError || !categoryData) {
          throw categoryError || new Error('Category not found.');
        }

        setCategory(categoryData);

        const { data: productsData, error: productsError } = await supabase
          .from('products')
          .select('*')
          .eq('category_id', categoryData.id)
          .eq('is_active', true);

        if (productsError) {
          throw productsError;
        }

        setProducts(productsData ?? []);
      } catch (fetchError) {
        console.error('Failed to load category or products.', fetchError);
        setErrorMessage('Failed to load category or products.');
        setCategory(null);
        setProducts([]);
      } finally {
        setLoading(false);
      }
    };

    fetchCategoryAndProducts();
  }, [slug]);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (errorMessage) {
    return (
      <div className="container mx-auto p-4">
        <div className="rounded-lg border border-red-200 bg-red-50 p-6 text-red-700">
          {errorMessage}
        </div>
      </div>
    );
  }

  if (!category) {
    return <div>Category not found.</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">{category.name}</h1>
      <p className="mb-4">{category.description}</p>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
};

export default CategoryPage;