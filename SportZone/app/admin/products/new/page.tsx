import { useState } from 'react';
import { supabase } from '@/lib/supabase';
import ProductForm from '@/components/admin/ProductForm';
import { useRouter } from 'next/router';

const NewProductPage = () => {
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (productData) => {
    setLoading(true);
    const { data, error } = await supabase
      .from('products')
      .insert([productData]);

    if (error) {
      alert('Error creating product: ' + error.message);
    } else {
      alert('Product created successfully!');
      router.push('/admin/products');
    }
    setLoading(false);
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Add New Product</h1>
      <ProductForm onSubmit={handleSubmit} loading={loading} />
    </div>
  );
};

export default NewProductPage;