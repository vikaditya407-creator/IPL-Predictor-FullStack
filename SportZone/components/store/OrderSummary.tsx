import React from 'react';

interface OrderSummaryProps {
  items: { name: string; price: number; quantity: number }[];
  subtotal: number;
  shipping: number;
  total: number;
}

const OrderSummary: React.FC<OrderSummaryProps> = ({ items, subtotal, shipping, total }) => {
  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-lg font-semibold mb-4">Order Summary</h2>
      <div className="space-y-2">
        {items.map((item, index) => (
          <div key={index} className="flex justify-between">
            <span>{item.name} (x{item.quantity})</span>
            <span>₹{item.price * item.quantity}</span>
          </div>
        ))}
      </div>
      <div className="flex justify-between mt-4">
        <span>Subtotal</span>
        <span>₹{subtotal}</span>
      </div>
      <div className="flex justify-between">
        <span>Shipping</span>
        <span>₹{shipping}</span>
      </div>
      <div className="border-t border-gray-300 mt-4 pt-2 flex justify-between font-semibold">
        <span>Total</span>
        <span>₹{total}</span>
      </div>
    </div>
  );
};

export default OrderSummary;