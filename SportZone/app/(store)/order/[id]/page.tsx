import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { supabase } from '@/lib/supabase';
import OrderSummary from '@/components/store/OrderSummary';
import { Toast } from '@/components/ui/Toast';

const OrderPage = () => {
  const router = useRouter();
  const { id } = router.query;
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [toast, setToast] = useState({ message: '', type: '' });

  useEffect(() => {
    const fetchOrder = async () => {
      if (!id) return;

      const { data, error } = await supabase
        .from('orders')
        .select('*')
        .eq('id', id)
        .single();

      if (error) {
        setError(error.message);
        setToast({ message: 'Failed to fetch order details.', type: 'error' });
      } else {
        setOrder(data);
      }
      setLoading(false);
    };

    fetchOrder();
  }, [id]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div className="container mx-auto p-4">
      {toast.message && <Toast message={toast.message} type={toast.type} />}
      <h1 className="text-2xl font-bold mb-4">Order Confirmation</h1>
      <p className="mb-2">Order ID: <strong>{order.id}</strong></p>
      <OrderSummary items={order.items} totalAmount={order.total_amount} />
      <p className="mt-4">Thank you for your purchase! Your order will be processed shortly.</p>
      <button
        onClick={() => router.push('/')}
        className="mt-4 bg-d85a30 text-white px-4 py-2 rounded"
      >
        Continue Shopping
      </button>
    </div>
  );
};

export default OrderPage;