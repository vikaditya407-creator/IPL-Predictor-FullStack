import React from 'react';
import { Order } from '../../types';

interface OrderRowProps {
  order: Order;
  onStatusChange: (orderId: number, status: string) => void;
}

const OrderRow: React.FC<OrderRowProps> = ({ order, onStatusChange }) => {
  const handleStatusChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    onStatusChange(order.id, event.target.value);
  };

  return (
    <tr>
      <td className="px-4 py-2 border-b">{order.id}</td>
      <td className="px-4 py-2 border-b">{order.customerName}</td>
      <td className="px-4 py-2 border-b">{new Date(order.createdAt).toLocaleDateString()}</td>
      <td className="px-4 py-2 border-b">{order.totalAmount}</td>
      <td className="px-4 py-2 border-b">
        <select
          value={order.status}
          onChange={handleStatusChange}
          className="border rounded p-1"
        >
          <option value="pending">Pending</option>
          <option value="shipped">Shipped</option>
          <option value="delivered">Delivered</option>
          <option value="cancelled">Cancelled</option>
        </select>
      </td>
    </tr>
  );
};

export default OrderRow;