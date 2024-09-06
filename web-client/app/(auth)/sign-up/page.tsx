'use client';

import { FormEvent, useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';

export default function SignUpPage() {
  const [form_data, set_form_data] = useState({
    first_name: '',
    last_name: '',
    address: '',
    dob: '',
    phone_number: '',
    email: '',
    password: '',
  });

  const handle_change = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    set_form_data(prev_state => ({
      ...prev_state,
      [name]: value
    }));
  };

  const handle_submit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    try {
      const response = await fetch('http://localhost:8000/api/users/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(form_data),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      console.log('Sign-up successful:', data);
      
    } catch (error) {
      console.error('Error during sign-up:', error);
     
    }
  };

  return (
    <div className="min-h-screen flex">
      <div className="w-1/2 relative">
        <Image
          src="/signup-image.jpg"
          alt="Sign up"
          layout="fill"
          objectFit="cover"
        />
      </div>
      <div className="w-1/2 flex items-center justify-center bg-white">
        <div className="max-w-md w-full p-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Create your account
          </h2>
          <form className="space-y-4" onSubmit={handle_submit}>
            {[
              { name: 'first_name', label: 'First name', type: 'text' },
              { name: 'last_name', label: 'Last name', type: 'text' },
              { name: 'address', label: 'Address', type: 'text' },
              { name: 'dob', label: 'Date of Birth', type: 'date' },
              { name: 'phone_number', label: 'Phone number', type: 'tel' },
              { name: 'email', label: 'Email', type: 'email' },
              { name: 'password', label: 'Password', type: 'password' },
            ].map((field) => (
              <div key={field.name}>
                <label htmlFor={field.name} className="block text-sm font-medium text-gray-700 mb-1">
                  {field.label}
                </label>
                <input
                  id={field.name}
                  name={field.name}
                  type={field.type}
                  required
                  className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  placeholder={`Enter your ${field.label.toLowerCase()}`}
                  value={form_data[field.name as keyof typeof form_data]}
                  onChange={handle_change}
                />
              </div>
            ))}
            <div className="flex items-center">
              <input
                id="terms"
                name="terms"
                type="checkbox"
                required
                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <label htmlFor="terms" className="ml-2 block text-xs text-gray-900">
                By creating an account means you agree to the <a href="#" className="text-indigo-600 hover:text-indigo-500">Terms and Conditions</a>, and our <a href="#" className="text-indigo-600 hover:text-indigo-500">Privacy Policy</a>
              </label>
            </div>
            <div>
              <button
                type="submit"
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-black hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
              >
                Sign Up
              </button>
            </div>
          </form>
          <div className="mt-6 text-center">
            <Link href="/login" className="font-medium text-indigo-600 hover:text-indigo-500">
              Already have an account? Sign in
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
