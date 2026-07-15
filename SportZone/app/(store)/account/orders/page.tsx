"use client";

import Link from 'next/link';
import Navbar from '@/components/store/Navbar';
import Footer from '@/components/store/Footer';

const OrdersPage = () => {
  // Mock orders data
  const mockOrders = [
    {
      id: 'ORD-001',
      date: '2024-04-15',
      status: 'Delivered',
      total: 2499,
      items: ['SG Scorer Classic Bat']
    },
    {
      id: 'ORD-002',
      date: '2024-04-10',
      status: 'In Transit',
      total: 1299,
      items: ['Nike Strike Football']
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-4xl mx-auto py-16 px-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">My Orders</h1>

        {mockOrders.length === 0 ? (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">📦</div>
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">No orders yet</h2>
            <p className="text-gray-600 mb-6">You haven't placed any orders yet.</p>
            <Link
              href="/"
              className="inline-block bg-[#D85A30] text-white px-8 py-3 rounded-lg font-semibold hover:bg-[#B84525] transition-colors"
            >
              Start Shopping
            </Link>
          </div>
        ) : (
          <div className="space-y-6">
            {mockOrders.map((order) => (
              <div key={order.id} className="bg-white rounded-lg shadow p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-lg font-semibold">Order #{order.id}</h3>
                    <p className="text-gray-600">Placed on {order.date}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-lg font-bold">₹{order.total}</p>
                    <span className={`inline-block px-2 py-1 rounded-full text-xs font-semibold ${
                      order.status === 'Delivered'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {order.status}
                    </span>
                  </div>
                </div>
                <div className="border-t pt-4">
                  <p className="text-sm text-gray-600">
                    Items: {order.items.join(', ')}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      <Footer />
    </div>
  );
};

export default OrdersPage;