import React from 'react';
import AdminSidebar from '@/components/admin/AdminSidebar';
import StatsCard from '@/components/admin/StatsCard';
import OrderRow from '@/components/admin/OrderRow';
import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase';

const AdminPage = () => {
  const [stats, setStats] = useState({ totalProducts: 0, ordersToday: 0, revenueToday: 0, lowStockCount: 0 });
  const [recentOrders, setRecentOrders] = useState([]);

  useEffect(() => {
    const fetchStats = async () => {
      const { data: productCount } = await supabase.from('products').select('*', { count: 'exact' });
      const { data: orders } = await supabase.from('orders').select('*').eq('created_at', new Date().toISOString().split('T')[0]);
      const revenue = orders.reduce((acc, order) => acc + order.total_amount, 0);
      const lowStock = await supabase.from('products').select('*').lt('stock_quantity', 5);

      setStats({
        totalProducts: productCount.length,
        ordersToday: orders.length,
        revenueToday: revenue,
        lowStockCount: lowStock.length,
      });
      setRecentOrders(orders.slice(0, 10));
    };

    fetchStats();
  }, []);

  return (
    <div className="flex">
      <AdminSidebar />
      <div className="flex-1 p-6">
        <h1 className="text-2xl font-bold mb-4">Admin Dashboard</h1>
        <div className="grid grid-cols-4 gap-4 mb-6">
          <StatsCard title="Total Products" value={stats.totalProducts} />
          <StatsCard title="Orders Today" value={stats.ordersToday} />
          <StatsCard title="Revenue Today" value={`₹${stats.revenueToday.toFixed(2)}`} />
          <StatsCard title="Low Stock Count" value={stats.lowStockCount} />
        </div>
        <h2 className="text-xl font-semibold mb-4">Recent Orders</h2>
        <table className="min-w-full bg-white border border-gray-300">
          <thead>
            <tr>
              <th className="py-2 px-4 border-b">Order ID</th>
              <th className="py-2 px-4 border-b">Customer</th>
              <th className="py-2 px-4 border-b">Date</th>
              <th className="py-2 px-4 border-b">Total</th>
              <th className="py-2 px-4 border-b">Status</th>
            </tr>
          </thead>
          <tbody>
            {recentOrders.map(order => (
              <OrderRow key={order.id} order={order} />
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AdminPage;