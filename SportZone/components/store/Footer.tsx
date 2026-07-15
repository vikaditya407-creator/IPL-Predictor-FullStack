import React from 'react';

const Footer = () => {
    return (
        <footer className="bg-gray-800 text-white py-6">
            <div className="container mx-auto text-center">
                <p className="mb-2">© {new Date().getFullYear()} SportZone. All rights reserved.</p>
                <p className="mb-2">Contact us: support@sportzone.com</p>
                <p className="mb-2">GST Number: 1234-5678-9012</p>
                <div className="flex justify-center space-x-4">
                    <a href="/terms" className="hover:underline">Terms of Service</a>
                    <a href="/privacy" className="hover:underline">Privacy Policy</a>
                </div>
            </div>
        </footer>
    );
};

export default Footer;