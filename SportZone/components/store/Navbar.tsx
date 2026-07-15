"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
// import { useSession } from '@supabase/auth-helpers-react';
import { useCart } from '@/lib/cart'; // Assuming you have a custom hook for cart management

const Navbar = () => {
    // const { session } = useSession();
    const session = null; // Placeholder until auth is implemented
    const { cartItems } = useCart(); // Custom hook to manage cart state
    const cartCount = cartItems.length;
    const [searchQuery, setSearchQuery] = useState('');
    const router = useRouter();

    const handleSearch = (e: React.FormEvent) => {
        e.preventDefault();
        if (searchQuery.trim()) {
            router.push(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
        }
    };

    return (
        <nav className="bg-white shadow">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between h-16">
                    <div className="flex">
                        <Link href="/" className="flex-shrink-0 flex items-center">
                            <span className="text-2xl font-bold text-[#D85A30]">SportZone</span>
                        </Link>
                        <div className="hidden sm:ml-6 sm:flex space-x-4">
                            <Link href="/category/cricket" className="text-gray-900 hover:bg-gray-200 px-3 py-2 rounded-md text-sm font-medium">Cricket</Link>
                            <Link href="/category/football" className="text-gray-900 hover:bg-gray-200 px-3 py-2 rounded-md text-sm font-medium">Football</Link>
                            <Link href="/category/fitness" className="text-gray-900 hover:bg-gray-200 px-3 py-2 rounded-md text-sm font-medium">Fitness</Link>
                            <Link href="/category/badminton" className="text-gray-900 hover:bg-gray-200 px-3 py-2 rounded-md text-sm font-medium">Badminton</Link>
                            <Link href="/category/running" className="text-gray-900 hover:bg-gray-200 px-3 py-2 rounded-md text-sm font-medium">Running</Link>
                        </div>
                    </div>
                    <div className="flex items-center">
                        <form onSubmit={handleSearch} className="flex items-center mr-4">
                            <input
                                type="text"
                                placeholder="Search products..."
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                className="px-3 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                            />
                            <button
                                type="submit"
                                className="px-4 py-2 bg-[#D85A30] text-white rounded-r-md hover:bg-[#B84525] transition-colors"
                            >
                                Search
                            </button>
                        </form>
                        <div className="relative">
                            <Link href="/wishlist" className="text-gray-900 hover:bg-gray-200 px-3 py-2 rounded-md text-sm font-medium">
                                Wishlist
                            </Link>
                        </div>
                        <div className="relative ml-4">
                            <Link href="/cart" className="text-gray-900 hover:bg-gray-200 px-3 py-2 rounded-md text-sm font-medium">
                                Cart
                                {cartCount > 0 && (
                                    <span className="absolute top-0 right-0 inline-flex items-center justify-center w-4 h-4 text-xs font-bold text-white bg-red-500 rounded-full">
                                        {cartCount}
                                    </span>
                                )}
                            </Link>
                        </div>
                        <div className="ml-4">
                            {session ? (
                                <Link href="/account/profile" className="text-gray-900 hover:bg-gray-200 px-3 py-2 rounded-md text-sm font-medium">
                                    {session.user.email}
                                </Link>
                            ) : (
                                <Link href="/account/login" className="text-gray-900 hover:bg-gray-200 px-3 py-2 rounded-md text-sm font-medium">
                                    Login
                                </Link>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;