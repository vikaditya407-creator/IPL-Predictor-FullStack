import { NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';
import Razorpay from 'razorpay';
import { v4 as uuidv4 } from 'uuid';

const razorpay = new Razorpay({
  key_id: process.env.NEXT_PUBLIC_RAZORPAY_KEY_ID,
  key_secret: process.env.RAZORPAY_KEY_SECRET,
});

export async function POST(req) {
  const { items, total_amount, user_id, shipping_address } = await req.json();

  // Create a Razorpay order
  const options = {
    amount: total_amount * 100, // amount in paise
    currency: 'INR',
    receipt: uuidv4(),
    payment_capture: 1,
  };

  try {
    const order = await razorpay.orders.create(options);
    
    // Save order to the database
    const { data, error } = await supabase
      .from('orders')
      .insert([
        {
          user_id,
          items,
          total_amount,
          status: 'pending',
          payment_id: order.id,
          payment_status: 'pending',
          shipping_address,
          gst_invoice_number: `SPZ-${new Date().getFullYear()}-${String(Math.floor(Math.random() * 10000)).padStart(4, '0')}`,
        },
      ]);

    if (error) throw error;

    return NextResponse.json({ order, success: true });
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}