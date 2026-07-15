import React from 'react';
import Image from 'next/image';
import Link from 'next/link';

interface Product {
  id: number;
  name: string;
  slug: string;
  price: number;
  mrp: number;
  images: string[];
  is_featured: boolean;
  stock_quantity: number;
}

interface ProductCardProps {
  product: Product;
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  const { id, name, slug, price, mrp, images, is_featured, stock_quantity } = product;
  const discount = Math.round(((mrp - price) / mrp) * 100);
  const stockIndicator = stock_quantity > 0 ? 'In Stock' : 'Out of Stock';

  return (
    <div className="border rounded-lg overflow-hidden shadow-lg">
      <Link href={`/product/${slug}`}>
        <div className="relative h-48 w-full">
          <Image
            src={images[0]}
            alt={name}
            fill
            style={{ objectFit: 'cover' }}
            className="transition-transform duration-300 hover:scale-105"
          />
        </div>
      </Link>
      <div className="p-4">
        <h3 className="text-lg font-semibold">{name}</h3>
        <p className="text-gray-500">{stockIndicator}</p>
        <div className="flex items-center justify-between mt-2">
          <span className="text-xl font-bold text-[#D85A30]">₹{price}</span>
          {discount > 0 && (
            <span className="text-sm text-gray-500 line-through">₹{mrp}</span>
          )}
        </div>
        {discount > 0 && (
          <span className="bg-green-500 text-white text-xs px-2 py-1 rounded-full mt-1">
            {discount}% Off
          </span>
        )}
      </div>
    </div>
  );
};

export default ProductCard;