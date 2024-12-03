"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { BarChart2, User } from "react-feather";

const AdminSidebar = () => {
  const pathname = usePathname();
  const locale = pathname.split("/")[1];

  const isActive = (path: string) => pathname === path;

  return (
    <div className="fixed top-0 left-0 h-full w-64 bg-gray-800 text-white p-5">
      <nav className="mt-8">
        <ul className="space-y-4">
          <li>
            <Link
              href={`/${locale}/admin`}
              className={`flex items-center space-x-2 hover:text-gray-300 ${
                isActive("/admin") ? "text-blue-400" : ""
              }`}
            >
              <BarChart2 size={20} />
              <span>Dashboard</span>
            </Link>
          </li>
          <li>
            <Link
              href={`/${locale}/admin/create-admin`}
              className={`flex items-center space-x-2 hover:text-gray-300 ${
                isActive("/admin/create-admin") ? "text-blue-400" : ""
              }`}
            >
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
