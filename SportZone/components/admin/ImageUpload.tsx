import { useState } from 'react';
import { supabase } from '../../lib/supabase';

const ImageUpload = ({ onUpload }) => {
  const [selectedImages, setSelectedImages] = useState([]);
  const [uploading, setUploading] = useState(false);

  const handleImageChange = (event) => {
    const files = Array.from(event.target.files);
    setSelectedImages(files);
  };

  const uploadImages = async () => {
    if (selectedImages.length === 0) return;

    setUploading(true);
    const imageUrls = [];

    for (const file of selectedImages) {
      const { data, error } = await supabase.storage
        .from('product-images')
        .upload(`public/${file.name}`, file, {
          cacheControl: '3600',
          upsert: true,
        });

      if (error) {
        console.error('Error uploading image:', error);
        setUploading(false);
        return;
      }

      const url = `${process.env.NEXT_PUBLIC_SUPABASE_URL}/storage/v1/object/public/product-images/${data.path}`;
      imageUrls.push(url);
    }

    setUploading(false);
    setSelectedImages([]);
    onUpload(imageUrls);
  };

  return (
    <div>
      <input
        type="file"
        accept="image/*"
        multiple
        onChange={handleImageChange}
        className="mb-4"
      />
      <button
        onClick={uploadImages}
        disabled={uploading}
        className={`bg-${uploading ? 'gray-400' : 'D85A30'} text-white px-4 py-2 rounded`}
      >
        {uploading ? 'Uploading...' : 'Upload Images'}
      </button>
      <div className="mt-4">
        {selectedImages.length > 0 && (
          <ul>
            {selectedImages.map((file, index) => (
              <li key={index}>{file.name}</li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default ImageUpload;