"use client";

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import Navbar from '@/components/store/Navbar';
import Footer from '@/components/store/Footer';
import { useCart } from '@/lib/cart';

interface Product {
  id: number;
  name: string;
  slug: string;
  description: string;
  specifications: Record<string, string>;
  price: number;
  mrp: number;
  images: string[];
  category_id: number;
  brand: string;
  sku: string;
  stock_quantity: number;
  is_featured: boolean;
}

const ProductDetailPage = () => {
  const params = useParams();
  const slug = params?.slug as string;
  const [product, setProduct] = useState<Product | null>(null);
  const [selectedImage, setSelectedImage] = useState(0);
  const [quantity, setQuantity] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const { addToCart } = useCart();

  // Mock product data - in real app, fetch from API
  const mockProducts: Product[] = [
    {
      id: 1,
      name: 'SG Scorer Classic Bat',
      slug: 'sg-scorer-classic-bat',
      description: 'A classic cricket bat for professional players. Made from premium willow wood with excellent balance and power.',
      specifications: {
        'Material': 'Willow',
        'Weight': '2.8 lbs',
        'Length': '33 inches',
        'Brand': 'SG'
      },
      price: 2499,
      mrp: 2999,
      images: [
        'https://images.unsplash.com/photo-1587174486073-ae18752afe6c?w=600&h=400&fit=crop',
        'https://images.unsplash.com/photo-1531415074968-036ba1b575da?w=600&h=400&fit=crop'
      ],
      category_id: 1,
      brand: 'SG',
      sku: 'SG-001',
      stock_quantity: 42,
      is_featured: true
    },
    {
      id: 2,
      name: 'Nike Strike Football',
      slug: 'nike-strike-football',
      description: 'Durable football for all weather conditions. Perfect for training and matches.',
      specifications: {
        'Material': 'Synthetic',
        'Size': '5',
        'Brand': 'Nike'
      },
      price: 1299,
      mrp: 1299,
      images: ['https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=600&h=400&fit=crop'],
      category_id: 2,
      brand: 'Nike',
      sku: 'NIKE-001',
      stock_quantity: 30,
      is_featured: true
    },
    {
      id: 3,
      name: 'Yonex Nanoray 7000I Racket',
      slug: 'yonex-nanoray-7000i-racket',
      description: 'Lightweight badminton racket for quick swings. Ideal for intermediate to advanced players.',
      specifications: {
        'Material': 'Graphite',
        'Weight': '4U',
        'Balance': 'Head Light',
        'Brand': 'Yonex'
      },
      price: 3199,
      mrp: 3800,
      images: ['https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=600&h=400&fit=crop'],
      category_id: 4,
      brand: 'Yonex',
      sku: 'YONEX-001',
      stock_quantity: 18,
      is_featured: true
    },
    {
      id: 4,
      name: 'Nivia 20kg Dumbbell Set',
      slug: 'nivia-20kg-dumbbell-set',
      description: 'Adjustable dumbbell set for home workouts. Includes dumbbells and rack.',
      specifications: {
        'Material': 'Cast Iron',
        'Weight': '20kg',
        'Brand': 'Nivia'
      },
      price: 1899,
      mrp: 1899,
      images: ['https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=600&h=400&fit=crop'],
      category_id: 3,
      brand: 'Nivia',
      sku: 'NIVIA-001',
      stock_quantity: 25,
      is_featured: true
    },
    {
      id: 5,
      name: 'Asics Gel-Nimbus 25 Shoes',
      slug: 'asics-gel-nimbus-25-shoes',
      description: 'Comfortable running shoes for long distances. Advanced cushioning technology.',
      specifications: {
        'Material': 'Mesh',
        'Size': 'Available in multiple sizes',
        'Technology': 'GEL Cushioning',
        'Brand': 'Asics'
      },
      price: 7499,
      mrp: 8999,
      images: ['https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&h=400&fit=crop'],
      category_id: 5,
      brand: 'Asics',
      sku: 'ASICS-001',
      stock_quantity: 11,
      is_featured: true
    },
    {
      id: 6,
      name: 'Adidas Predator Football Boots',
      slug: 'adidas-predator-football-boots',
      description: 'Professional football boots with advanced grip technology. Perfect for competitive play.',
      specifications: {
        'Material': 'Synthetic',
        'Technology': 'Predator Grip',
        'Brand': 'Adidas'
      },
      price: 8999,
      mrp: 10999,
      images: ['https://images.unsplash.com/photo-1543326727-cf6c39e8f84c?w=600&h=400&fit=crop'],
      category_id: 2,
      brand: 'Adidas',
      sku: 'ADIDAS-001',
      stock_quantity: 15,
      is_featured: true
    }
  ];

  useEffect(() => {
    if (!slug) {
      setIsLoading(false);
      return;
    }

    setIsLoading(true);
    // Simulate API call delay
    const timer = setTimeout(() => {
      const foundProduct = mockProducts.find(p => p.slug === slug);
      setProduct(foundProduct || null);
      setSelectedImage(0);
      setQuantity(1);
      setIsLoading(false);
    }, 100); // Small delay to show loading state

    return () => clearTimeout(timer);
  }, [slug]);

  const handleAddToCart = () => {
    if (!product) {
      alert('Product information is not available.');
      return;
    }

    if (isOutOfStock) {
      alert('This product is currently out of stock.');
      return;
    }

    if (quantity > product.stock_quantity) {
      alert(`Only ${product.stock_quantity} items available in stock.`);
      return;
    }

    if (quantity <= 0) {
      alert('Please select a valid quantity.');
      return;
    }

    addToCart({
      id: String(product.id),
      name: product.name || 'Unknown Product',
      price: product.price || 0,
      quantity: quantity
    });
    alert(`Added ${quantity} ${product.name || 'item'}(s) to cart!`);
  };

  const handleImageError = (index: number) => {
    console.warn(`Failed to load image at index ${index} for product ${product?.name || 'unknown'}`);
  };

  // Loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="max-w-7xl mx-auto py-8 px-4">
          <div className="animate-pulse">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="space-y-4">
                <div className="aspect-square bg-gray-200 rounded-lg"></div>
                <div className="flex space-x-2">
                  {[...Array(3)].map((_, i) => (
                    <div key={i} className="w-20 h-20 bg-gray-200 rounded"></div>
                  ))}
                </div>
              </div>
              <div className="space-y-6">
                <div className="space-y-2">
                  <div className="h-8 bg-gray-200 rounded w-3/4"></div>
                  <div className="h-4 bg-gray-200 rounded w-full"></div>
                  <div className="h-4 bg-gray-200 rounded w-2/3"></div>
                </div>
                <div className="h-12 bg-gray-200 rounded w-1/2"></div>
                <div className="h-12 bg-gray-200 rounded w-full"></div>
              </div>
            </div>
          </div>
        </div>
        <Footer />
      </div>
    );
  }

  if (!product) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex flex-col justify-center items-center h-64 space-y-4">
          <div className="text-6xl">🔍</div>
          <h1 className="text-2xl font-bold text-gray-900">Product Not Found</h1>
          <p className="text-gray-600">The product you're looking for doesn't exist.</p>
          <Link
            href="/"
            className="bg-[#D85A30] text-white px-6 py-2 rounded-lg hover:bg-[#B84525] transition-colors"
          >
            Back to Home
          </Link>
        </div>
        <Footer />
      </div>
    );
  }

  const discount = product.mrp > product.price ? Math.round(((product.mrp - product.price) / product.mrp) * 100) : 0;
  const maxQuantity = Math.min(product.stock_quantity, 10); // Limit to 10 or available stock
  const isOutOfStock = product.stock_quantity === 0;

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <div className="max-w-7xl mx-auto py-8 px-4">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Product Images */}
          <div className="space-y-4">
            <div className="aspect-square relative overflow-hidden rounded-lg bg-gray-100">
              {product.images && product.images.length > 0 && selectedImage < product.images.length ? (
                <Image
                  src={product.images[selectedImage]}
                  alt={product.name}
                  fill
                  className="object-cover"
                  onError={() => handleImageError(selectedImage)}
                  priority
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center text-gray-400">
                  <span className="text-4xl">📦</span>
                </div>
              )}
            </div>
            {product.images && product.images.length > 1 && (
              <div className="flex space-x-2 overflow-x-auto">
                {product.images.map((image, index) => (
                  <button
                    key={index}
                    onClick={() => setSelectedImage(index)}
                    className={`flex-shrink-0 w-20 h-20 relative overflow-hidden rounded border-2 transition-colors ${
                      selectedImage === index ? 'border-blue-500' : 'border-gray-300 hover:border-gray-400'
                    }`}
                    aria-label={`View image ${index + 1} of ${product.name}`}
                  >
                    <Image
                      src={image}
                      alt={`${product.name} - Image ${index + 1}`}
                      fill
                      className="object-cover"
                      onError={() => handleImageError(index)}
                    />
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Product Details */}
          <div className="space-y-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{product.name}</h1>
              <p className="text-lg text-gray-600 mt-2">{product.description}</p>
            </div>

            <div className="flex items-center space-x-4">
              <span className="text-3xl font-bold text-[#D85A30]">₹{product.price}</span>
              {discount > 0 && (
                <>
                  <span className="text-xl text-gray-500 line-through">₹{product.mrp}</span>
                  <span className="bg-green-500 text-white px-2 py-1 rounded-full text-sm">
                    {discount}% Off
                  </span>
                </>
              )}
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Quantity
                </label>
                <div className="flex items-center space-x-3">
                  <button
                    onClick={() => setQuantity(Math.max(1, quantity - 1))}
                    className="w-8 h-8 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    disabled={quantity <= 1 || isOutOfStock}
                    aria-label="Decrease quantity"
                  >
                    -
                  </button>
                  <span className="text-xl font-semibold min-w-[2rem] text-center">{quantity}</span>
                  <button
                    onClick={() => setQuantity(Math.min(maxQuantity, quantity + 1))}
                    className="w-8 h-8 rounded-full bg-gray-200 hover:bg-gray-300 flex items-center justify-center transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    disabled={quantity >= maxQuantity || isOutOfStock}
                    aria-label="Increase quantity"
                  >
                    +
                  </button>
                </div>
                <p className="text-sm text-gray-500 mt-1">
                  {isOutOfStock
                    ? 'Out of stock'
                    : product.stock_quantity <= 10
                      ? `${product.stock_quantity} available`
                      : `Limited to ${maxQuantity} per order`
                  }
                </p>
              </div>

              <button
                onClick={handleAddToCart}
                disabled={isOutOfStock}
                className="w-full bg-[#D85A30] text-white py-3 px-6 rounded-lg font-semibold hover:bg-[#B84525] transition-colors disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-[#D85A30]"
                aria-label={isOutOfStock ? 'Product out of stock' : `Add ${quantity} ${product.name} to cart`}
              >
                {isOutOfStock
                  ? 'Out of Stock'
                  : `Add to Cart - ₹${(product.price * quantity).toLocaleString()}`
                }
              </button>
            </div>

            {/* Specifications */}
            {product.specifications && Object.keys(product.specifications).length > 0 && (
              <div>
                <h3 className="text-lg font-semibold mb-3">Specifications</h3>
                <div className="space-y-2">
                  {Object.entries(product.specifications).map(([key, value]) => (
                    <div key={key} className="flex justify-between py-2 border-b border-gray-200">
                      <span className="font-medium">{key}:</span>
                      <span>{value || 'N/A'}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div className="text-sm text-gray-600 space-y-1">
              <p><strong>Brand:</strong> {product.brand || 'N/A'}</p>
              <p><strong>SKU:</strong> {product.sku || 'N/A'}</p>
              <p><strong>Stock:</strong> {
                product.stock_quantity > 0
                  ? `${product.stock_quantity} available`
                  : 'Out of stock'
              }</p>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default ProductDetailPage;