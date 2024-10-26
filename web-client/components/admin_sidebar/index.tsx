import React, { useState } from 'react';
import Link from 'next/link';
import { Menu, X, User, BarChart2, Package, ShoppingCart } from 'react-feather';

const AdminSidebar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <>
      <button
        className="fixed top-4 left-4 z-50 p-2 bg-black text-white rounded-md"
        onClick={toggleSidebar}
      >
        {isOpen ? <X size={24} /> : <Menu size={24} />}
      </button>
      <div
        className={`fixed top-0 left-0 h-full w-64 bg-gray-800 text-white p-5 transform transition-transform duration-300 ease-in-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <nav className="mt-16">
          <ul className="space-y-4">
            <li>
              <Link href="/admin/dashboard" className="flex items-center space-x-2 hover:text-gray-300">
                <BarChart2 size={20} />
                <span>Dashboard</span>
              </Link>
            </li>
            <li>
              <Link href="/admin/products" className="flex items-center space-x-2 hover:text-gray-300">
                <Package size={20} />
                <span>Products</span>
              </Link>
            </li>
            <li>
              <Link href="/admin/orders" className="flex items-center space-x-2 hover:text-gray-300">
                <ShoppingCart size={20} />
                <span>Orders</span>
              </Link>
            </li>
            <li>
              <Link href="/admin/create-admin" className="flex items-center space-x-2 hover:text-gray-300">
                <User size={20} />
                <span>Create Admin</span>
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </>
  );
};

export default AdminSidebar;
