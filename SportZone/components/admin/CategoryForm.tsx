import React, { useState } from 'react';
import { supabase } from '../../lib/supabase';
import { useRouter } from 'next/router';

const CategoryForm = ({ category }) => {
  const [name, setName] = useState(category ? category.name : '');
  const [slug, setSlug] = useState(category ? category.slug : '');
  const [description, setDescription] = useState(category ? category.description : '');
  const [image, setImage] = useState(null);
  const router = useRouter();

  const handleImageUpload = (e) => {
    setImage(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    let imageUrl = '';

    if (image) {
      const { data, error } = await supabase.storage
        .from('category-images')
        .upload(`public/${image.name}`, image);

      if (error) {
        console.error('Image upload error:', error);
        return;
      }
      imageUrl = data.Key;
    }

    const { error } = await supabase
      .from('categories')
      .upsert({
        id: category ? category.id : undefined,
        name,
        slug,
        description,
        image_url: imageUrl,
      });

    if (error) {
      console.error('Error saving category:', error);
    } else {
      router.push('/admin/categories');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700">Category Name</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-opacity-50"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">Slug</label>
        <input
          type="text"
          value={slug}
          onChange={(e) => setSlug(e.target.value)}
          required
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-opacity-50"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">Description</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-opacity-50"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700">Category Image</label>
        <input
          type="file"
          accept="image/*"
          onChange={handleImageUpload}
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-opacity-50"
        />
      </div>
      <button type="submit" className="mt-4 bg-blue-600 text-white py-2 px-4 rounded-md">
        {category ? 'Update Category' : 'Add Category'}
      </button>
    </form>
  );
};

export default CategoryForm;