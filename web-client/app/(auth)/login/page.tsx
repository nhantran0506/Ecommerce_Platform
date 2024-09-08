'use client';

import { useState, FormEvent } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { useRouter } from 'next/navigation';
import { API_BASE_URL, API_ROUTES } from '@/libraries/api';

export default function LoginPage() {
  const [form_data, set_form_data] = useState({
    user_name: '',
    password: '',
  });
  const [error, set_error] = useState('');
  const router = useRouter();

  const handle_change = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    set_form_data(prev_state => ({
      ...prev_state,
      [name]: value
    }));
  };

  const handle_submit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    set_error('');
    
    try {
      const response = await fetch(`${API_BASE_URL}${API_ROUTES.LOGIN}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(form_data),

      });
      if (!response.ok) {
        throw new Error('Login failed');
      }

      const data = await response.json();
      
      localStorage.setItem('token', data.token);
      router.push('/');
    } catch (error) {
      set_error('Invalid credentials. Please try again.');
    }
  };

  return (
    <div className="min-h-screen flex">
      <div className="w-1/2 relative">
        <Image
          src="/login-image.jpg"
          alt="Login"
          layout="fill"
          objectFit="cover"
        />
      </div>
      <div className="w-1/2 flex items-center justify-center bg-white">
        <div className="max-w-md w-full p-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back!
          </h2>
          <form className="space-y-4" onSubmit={handle_submit}>
            <div>
              <label htmlFor="user_name" className="block text-sm font-medium text-gray-700 mb-1">
                E-mail or phone number
              </label>
              <input
                id="user_name"
                name="user_name"
                type="text"
                required
                className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="Type your e-mail or phone number"
                value={form_data.user_name}
                onChange={handle_change}
              />
            </div>
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                required
                className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="Type your password"
                value={form_data.password}
                onChange={handle_change}
              />
            </div>
            <div className="flex items-center justify-end">
              <Link href="/forgot-password" className="text-sm text-indigo-600 hover:text-indigo-500">
                Forgot Password?
              </Link>
            </div>
            <div>
              <button
                type="submit"
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-black hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
              >
                Sign In
              </button>
            </div>
          </form>
          <div className="mt-6">
            <p className="text-center text-sm text-gray-500">or do it via other accounts</p>
            <div className="mt-4 flex justify-center space-x-4">
              <button className="p-2 border border-gray-300 rounded-full">
                <Image src="/google-icon.png" alt="Google" width={24} height={24} />
              </button>
              <button className="p-2 border border-gray-300 rounded-full">
                <Image src="/zalo-icon.png" alt="Zalo" width={24} height={24} />
              </button>
              <button className="p-2 border border-gray-300 rounded-full">
                <Image src="/facebook-icon.png" alt="Facebook" width={24} height={24} />
              </button>
            </div>
          </div>
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Don't have an account?{' '}
              <Link href="/sign-up" className="font-medium text-indigo-600 hover:text-indigo-500">
                Sign Up
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}