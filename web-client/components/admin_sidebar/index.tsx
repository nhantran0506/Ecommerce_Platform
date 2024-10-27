import React from 'react';
import Link from 'next/link';
import { BarChart2, User } from 'react-feather';

const AdminSidebar = () => {
  return (
    <div className="fixed top-0 left-0 h-full w-64 bg-gray-800 text-white p-5">
      <nav className="mt-8">
        <ul className="space-y-4">
          <li>
            <Link href="/admin" className="flex items-center space-x-2 hover:text-gray-300">
              <BarChart2 size={20} />
              <span>Dashboard</span>
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
  );
};

export default AdminSidebar;
