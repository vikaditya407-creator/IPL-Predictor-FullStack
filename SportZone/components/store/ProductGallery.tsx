import Image from 'next/image';

interface ProductGalleryProps {
  images: string[];
}

const ProductGallery: React.FC<ProductGalleryProps> = ({ images }) => {
  return (
    <div className="flex flex-col items-center">
      <div className="relative w-full h-96">
        {images.length > 0 ? (
          <Image
            src={images[0]}
            alt="Product Image"
            fill
            style={{ objectFit: 'contain' }}
            className="rounded-lg"
          />
        ) : (
          <div className="flex items-center justify-center w-full h-full bg-gray-200 rounded-lg">
            <span>No images available</span>
          </div>
        )}
      </div>
      <div className="flex space-x-2 mt-4">
        {images.map((image, index) => (
          <div key={index} className="w-24 h-24 relative cursor-pointer">
            <Image
              src={image}
              alt={`Thumbnail ${index + 1}`}
              fill
              style={{ objectFit: 'cover' }}
              className="rounded-lg"
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProductGallery;