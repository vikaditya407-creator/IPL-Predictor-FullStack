import React from 'react';
import Link from 'next/link';

interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
  image_url: string;
}

interface CategoryCardProps {
  category: Category;
}

const CategoryCard: React.FC<CategoryCardProps> = ({ category }) => {
  const { name, slug, image_url } = category;
  return (
    <Link href={`/category/${slug}`} className="group block overflow-hidden rounded-lg shadow-lg">
      <div className="relative">
        <img src={image_url} alt={name} className="w-full h-40 object-cover transition-transform duration-300 group-hover:scale-105" />
        <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 transition-opacity duration-300 opacity-0 group-hover:opacity-100">
          <h3 className="text-white text-lg font-semibold">{name}</h3>
        </div>
      </div>
    </Link>
  );
};

export default CategoryCard;