import React from 'react';
import { Inter } from 'next/font/google';
import './globals.css';
import Navbar from '../components/store/Navbar';
import Footer from '../components/store/Footer';
import { CartProvider } from '../lib/cart';

const inter = Inter({ subsets: ['latin'] });

export const metadata = {
  title: 'SportZone - Your Sports Equipment Store',
  description: 'Shop the best sports equipment at SportZone.',
};

const RootLayout = ({ children }) => {
  return (
    <html lang="en">
      <body className={inter.className}>
        <CartProvider>
          <Navbar />
          <main>{children}</main>
          <Footer />
        </CartProvider>
      </body>
    </html>
  );
};

export default RootLayout;