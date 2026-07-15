import { NextResponse } from 'next/server';
import { supabase } from '@/lib/supabase';
import crypto from 'crypto';

export async function POST(req: Request) {
    const { payment_id, order_id, signature } = await req.json();

    const order = await supabase
        .from('orders')
        .select('*')
        .eq('id', order_id)
        .single();

    if (!order.data) {
        return NextResponse.json({ error: 'Order not found' }, { status: 404 });
    }

    const key = process.env.RAZORPAY_KEY_SECRET;
    const generated_signature = crypto
        .createHmac('sha256', key)
        .update(`${order_id}|${payment_id}`)
        .digest('hex');

    if (generated_signature !== signature) {
        return NextResponse.json({ error: 'Invalid signature' }, { status: 400 });
    }

    const { error } = await supabase
        .from('orders')
        .update({ payment_status: 'confirmed', payment_id: payment_id })
        .eq('id', order_id);

    if (error) {
        return NextResponse.json({ error: 'Failed to update order' }, { status: 500 });
    }

    return NextResponse.json({ success: true });
}