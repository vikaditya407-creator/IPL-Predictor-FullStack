import React, { useEffect, useState } from 'react';
import { supabase } from '../../lib/supabase';
import ImageUpload from './ImageUpload';
import { Product } from '../../types';

interface ProductFormProps {
  product?: Product;
  onSave: (product: Product) => void;
}

const ProductForm: React.FC<ProductFormProps> = ({ product, onSave }) => {
  const [name, setName] = useState<string>('');
  const [slug, setSlug] = useState<string>('');
  const [description, setDescription] = useState<string>('');
  const [specifications, setSpecifications] = useState<{ [key: string]: string }>({});
  const [price, setPrice] = useState<number>(0);
  const [mrp, setMrp] = useState<number>(0);
  const [stockQuantity, setStockQuantity] = useState<number>(0);
  const [brand, setBrand] = useState<string>('');
  const [sku, setSku] = useState<string>('');
  const [isActive, setIsActive] = useState<boolean>(true);
  const [isFeatured, setIsFeatured] = useState<boolean>(false);
  const [images, setImages] = useState<string[]>([]);

  useEffect(() => {
    if (product) {
      setName(product.name);
      setSlug(product.slug);
      setDescription(product.description);
      setSpecifications(product.specifications);
      setPrice(product.price);
      setMrp(product.mrp);
      setStockQuantity(product.stock_quantity);
      setBrand(product.brand);
      setSku(product.sku);
      setIsActive(product.is_active);
      setIsFeatured(product.is_featured);
      setImages(product.images);
    }
  }, [product]);

  const handleSave = async () => {
    const newProduct = {
      name,
      slug,
      description,
      specifications,
      price,
      mrp,
      stock_quantity: stockQuantity,
      brand,
      sku,
      is_active: isActive,
      is_featured: isFeatured,
      images,
    };

    if (product) {
      await supabase
        .from('products')
        .update(newProduct)
        .eq('id', product.id);
    } else {
      await supabase.from('products').insert(newProduct);
    }

    onSave(newProduct);
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">{product ? 'Edit Product' : 'Add Product'}</h2>
      <div className="mb-4">
        <label className="block mb-1">Product Name</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="border p-2 w-full"
          required
        />
      </div>
      <div className="mb-4">
        <label className="block mb-1">Slug</label>
        <input
          type="text"
          value={slug}
          onChange={(e) => setSlug(e.target.value)}
          className="border p-2 w-full"
          required
        />
      </div>
      <div className="mb-4">
        <label className="block mb-1">Description</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="border p-2 w-full"
          required
        />
      </div>
      <div className="mb-4">
        <label className="block mb-1">Specifications</label>
        <textarea
          value={JSON.stringify(specifications)}
          onChange={(e) => setSpecifications(JSON.parse(e.target.value))}
          className="border p-2 w-full"
          placeholder='{"key": "value"}'
        />
      </div>
      <div className="mb-4">
        <label className="block mb-1">Price</label>
        <input
          type="number"
          value={price}
          onChange={(e) => setPrice(Number(e.target.value))}
          className="border p-2 w-full"
          required
        />
      </div>
      <div className="mb-4">
        <label className="block mb-1">MRP</label>
        <input
          type="number"
          value={mrp}
          onChange={(e) => setMrp(Number(e.target.value))}
          className="border p-2 w-full"
          required
        />
      </div>
      <div className="mb-4">
        <label className="block mb-1">Stock Quantity</label>
        <input
          type="number"
          value={stockQuantity}
          onChange={(e) => setStockQuantity(Number(e.target.value))}
          className="border p-2 w-full"
          required
        />
      </div>
      <div className="mb-4">
        <label className="block mb-1">Brand</label>
        <input
          type="text"
          value={brand}
          onChange={(e) => setBrand(e.target.value)}
          className="border p-2 w-full"
          required
        />
      </div>
      <div className="mb-4">
        <label className="block mb-1">SKU</label>
        <input
          type="text"
          value={sku}
          onChange={(e) => setSku(e.target.value)}
          className="border p-2 w-full"
          required
        />
      </div>
      <div className="mb-4">
        <label className="flex items-center">
          <input
            type="checkbox"
            checked={isActive}
            onChange={(e) => setIsActive(e.target.checked)}
          />
          Active
        </label>
      </div>
      <div className="mb-4">
        <label className="flex items-center">
          <input
            type="checkbox"
            checked={isFeatured}
            onChange={(e) => setIsFeatured(e.target.checked)}
          />
          Featured
        </label>
      </div>
      <ImageUpload images={images} setImages={setImages} />
      <button
        onClick={handleSave}
        className="bg-blue-500 text-white p-2 rounded"
      >
        Save
      </button>
    </div>
  );
};

export default ProductForm;