import { useEffect, useState } from 'react';
import { supabase } from '../../../lib/supabase';
import AdminSidebar from '../../../components/admin/AdminSidebar';
import { Customer } from '../../../types';

const CustomersPage = () => {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCustomers = async () => {
      const { data, error } = await supabase
        .from('users') // Assuming you have a 'users' table for customer data
        .select('id, name, email, created_at, orders_count, total_spent')
        .order('created_at', { ascending: false });

      if (error) {
        console.error('Error fetching customers:', error);
      } else {
        setCustomers(data);
      }
      setLoading(false);
    };

    fetchCustomers();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="flex">
      <AdminSidebar />
      <div className="flex-1 p-4">
        <h1 className="text-2xl font-bold mb-4">Customers</h1>
        <table className="min-w-full bg-white border border-gray-300">
          <thead>
            <tr>
              <th className="border-b p-2">Name</th>
              <th className="border-b p-2">Email</th>
              <th className="border-b p-2">Total Orders</th>
              <th className="border-b p-2">Total Spent</th>
              <th className="border-b p-2">Joined Date</th>
            </tr>
          </thead>
          <tbody>
            {customers.map((customer) => (
              <tr key={customer.id}>
                <td className="border-b p-2">{customer.name}</td>
                <td className="border-b p-2">{customer.email}</td>
                <td className="border-b p-2">{customer.orders_count}</td>
                <td className="border-b p-2">{customer.total_spent}</td>
                <td className="border-b p-2">{new Date(customer.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CustomersPage;