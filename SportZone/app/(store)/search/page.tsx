import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { supabase } from '../../../lib/supabase';
import ProductCard from '../../../components/store/ProductCard';
import Skeleton from '../../../components/ui/Skeleton';

const SearchPage = () => {
  const router = useRouter();
  const { q } = router.query;
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      if (q) {
        setLoading(true);
        const { data, error } = await supabase
          .from('products')
          .select('*')
          .ilike('name', `%${q}%`)
          .or(`ilike(description, '%${q}%')`)
          .limit(12);

        if (error) {
          console.error('Error fetching products:', error);
        } else {
          setProducts(data);
        }
        setLoading(false);
      }
    };

    fetchProducts();
  }, [q]);

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Search Results for: {q}</h1>
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 12 }).map((_, index) => (
            <Skeleton key={index} />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {products.length > 0 ? (
            products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))
          ) : (
            <p>No products found.</p>
          )}
        </div>
      )}
    </div>
  );
};

export default SearchPage;