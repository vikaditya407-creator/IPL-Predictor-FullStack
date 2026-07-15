"use client";

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { supabase } from '@/lib/supabase';
import ProductGallery from '@/components/store/ProductGallery';
import { Product } from '@/types';

const ProductPage = () => {
  const params = useParams();
  const slug = params?.slug as string | undefined;
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [relatedProducts, setRelatedProducts] = useState<Product[]>([]);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!slug) return;

    const fetchProduct = async () => {
      setLoading(true);
      setErrorMessage(null);

      try {
        const { data, error } = await supabase
          .from('products')
          .select('*')
          .eq('slug', slug)
          .single();

        if (error || !data) {
          setErrorMessage(error?.message || 'Product not found.');
          setProduct(null);
          return;
        }

        setProduct(data);

        const { data: relatedData, error: relatedError } = await supabase
          .from('products')
          .select('*')
          .eq('category_id', data.category_id)
          .neq('slug', slug)
          .limit(4);

        if (relatedError) {
          console.error('Error fetching related products:', relatedError);
          setRelatedProducts([]);
        } else {
          setRelatedProducts(relatedData ?? []);
        }
      } catch (fetchError) {
        console.error('Error fetching product:', fetchError);
        setErrorMessage('Unable to load product details.');
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
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

  if (!product) {
    return <div>Product not found</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <ProductGallery images={product.images} />
      <h1 className="text-2xl font-bold">{product.name}</h1>
      <p className="text-lg text-gray-600">{product.brand}</p>
      <p className="text-xl font-semibold">₹{product.price}</p>
      <p className="line-through text-gray-500">MRP: ₹{product.mrp}</p>
      <p className="mt-2">{product.description}</p>
      <div className="mt-4">
        <h2 className="text-lg font-semibold">Specifications</h2>
        <ul>
          {Object.entries(product.specifications).map(([key, value]) => (
            <li key={key}>
              <strong>{key}:</strong> {value}
            </li>
          ))}
        </ul>
      </div>
      <div className="mt-4">
        <h2 className="text-lg font-semibold">Related Products</h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {relatedProducts.map((relatedProduct) => (
            <div key={relatedProduct.id} className="border p-4">
              <img src={relatedProduct.images[0]} alt={relatedProduct.name} className="w-full h-32 object-cover" />
              <h3 className="text-lg font-semibold">{relatedProduct.name}</h3>
              <p className="text-xl font-semibold">₹{relatedProduct.price}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ProductPage;