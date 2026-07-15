import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { supabase } from '@/lib/supabase';
import ProductForm from '@/components/admin/ProductForm';
import { Product } from '@/types';

const EditProductPage = () => {
  const router = useRouter();
  const { id } = router.query;
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProduct = async () => {
      if (id) {
        const { data, error } = await supabase
          .from('products')
          .select('*')
          .eq('id', id)
          .single();

        if (error) {
          console.error('Error fetching product:', error);
        } else {
          setProduct(data);
        }
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  const handleUpdate = async (updatedProduct: Product) => {
    const { error } = await supabase
      .from('products')
      .update(updatedProduct)
      .eq('id', id);

    if (error) {
      console.error('Error updating product:', error);
    } else {
      router.push('/admin/products');
    }
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!product) {
    return <div>Product not found</div>;
  }

  return (
    <div>
      <h1>Edit Product</h1>
      <ProductForm product={product} onSubmit={handleUpdate} />
    </div>
  );
};

export default EditProductPage;