export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
  image_url: string;
  created_at: string;
}

export interface Product {
  id: number;
  name: string;
  slug: string;
  description: string;
  specifications: Record<string, any>;
  price: number;
  mrp: number;
  images: string[];
  category_id: number;
  brand: string;
  sku: string;
  stock_quantity: number;
  is_active: boolean;
  is_featured: boolean;
  created_at: string;
  updated_at: string;
}

export interface Order {
  id: number;
  user_id: number;
  items: Record<string, any>;
  total_amount: number;
  status: string;
  payment_id: string;
  payment_status: string;
  shipping_address: Record<string, any>;
  gst_invoice_number: string;
  created_at: string;
}

export interface CartItem {
  id: number;
  user_id: number;
  product_id: number;
  quantity: number;
  created_at: string;
}

export interface WishlistItem {
  id: number;
  user_id: number;
  product_id: number;
  created_at: string;
}

export interface AdminUser {
  id: number;
  user_id: number;
  created_at: string;
}