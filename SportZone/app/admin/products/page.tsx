import { useEffect, useState } from 'react';
import { supabase } from '../../../lib/supabase';
import AdminSidebar from '../../../components/admin/AdminSidebar';
import StatsCard from '../../../components/admin/StatsCard';
import { Product } from '../../../types';

const ProductsPage = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchProducts = async () => {
      const { data, error } = await supabase
        .from('products')
        .select('*')
        .ilike('name', `%${searchTerm}%`)
        .order('created_at', { ascending: false });

      if (error) {
        console.error('Error fetching products:', error);
      } else {
        setProducts(data);
      }
      setLoading(false);
    };

    fetchProducts();
  }, [searchTerm]);

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(e.target.value);
  };

  return (
    <div className="flex">
      <AdminSidebar />
      <div className="flex-1 p-6">
        <h1 className="text-2xl font-bold mb-4">Products</h1>
        <input
          type="text"
          placeholder="Search products..."
          value={searchTerm}
          onChange={handleSearchChange}
          className="border p-2 rounded mb-4"
        />
        {loading ? (
          <div>Loading...</div>
        ) : (
          <table className="min-w-full bg-white border border-gray-300">
            <thead>
              <tr>
                <th className="border-b p-2">Thumbnail</th>
                <th className="border-b p-2">Name</th>
                <th className="border-b p-2">Category</th>
                <th className="border-b p-2">Price</th>
                <th className="border-b p-2">Stock</th>
                <th className="border-b p-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {products.map((product) => (
                <tr key={product.id}>
                  <td className="border-b p-2">
                    <img src={product.images[0]} alt={product.name} className="w-16 h-16" />
                  </td>
                  <td className="border-b p-2">{product.name}</td>
                  <td className="border-b p-2">{product.category_id}</td>
                  <td className="border-b p-2">₹{product.price}</td>
                  <td className="border-b p-2">{product.stock_quantity}</td>
                  <td className="border-b p-2">
                    <button className="text-blue-500">Edit</button>
                    <button className="text-red-500 ml-2">Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default ProductsPage;