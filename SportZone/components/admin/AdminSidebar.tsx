import React from 'react';
import Link from 'next/link';

const AdminSidebar: React.FC = () => {
    return (
        <div className="bg-gray-800 text-white w-64 h-full p-5">
            <h2 className="text-xl font-bold mb-5">Admin Panel</h2>
            <ul className="space-y-2">
                <li>
                    <Link href="/admin" className="block p-2 hover:bg-gray-700 rounded">
                        Dashboard
                    </Link>
                </li>
                <li>
                    <Link href="/admin/products" className="block p-2 hover:bg-gray-700 rounded">
                        Products
                    </Link>
                </li>
                <li>
                    <Link href="/admin/categories" className="block p-2 hover:bg-gray-700 rounded">
                        Categories
                    </Link>
                </li>
                <li>
                    <Link href="/admin/orders" className="block p-2 hover:bg-gray-700 rounded">
                        Orders
                    </Link>
                </li>
                <li>
                    <Link href="/admin/customers" className="block p-2 hover:bg-gray-700 rounded">
                        Customers
                    </Link>
                </li>
            </ul>
        </div>
    );
};

export default AdminSidebar;