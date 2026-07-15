import React from 'react';
import Image from 'next/image';
import { useCart } from '../../lib/cart'; // Assuming you have a cart context or hook
import { CartItemType } from '../../types'; // Assuming you have a type for cart items

interface CartItemProps {
  item: CartItemType;
}

const CartItem: React.FC<CartItemProps> = ({ item }) => {
  const { removeFromCart, updateQuantity } = useCart();

  const handleQuantityChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    updateQuantity(item.id, Number(e.target.value));
  };

  return (
    <div className="flex items-center justify-between p-4 border-b">
      <div className="flex items-center">
        <Image src={item.image} alt={item.name} width={100} height={100} className="mr-4" />
        <div>
          <h3 className="text-lg font-semibold">{item.name}</h3>
          <p className="text-gray-600">Price: ₹{item.price}</p>
        </div>
      </div>
      <div className="flex items-center">
        <select value={item.quantity} onChange={handleQuantityChange} className="border rounded p-1">
          {[...Array(item.stockQuantity).keys()].map((x) => (
            <option key={x} value={x + 1}>
              {x + 1}
            </option>
          ))}
        </select>
        <button onClick={() => removeFromCart(item.id)} className="ml-4 text-red-500">
          Remove
        </button>
      </div>
    </div>
  );
};

export default CartItem;