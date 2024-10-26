"use client";

import { useState } from 'react';
import { Button, Input } from "@nextui-org/react";
import { API_BASE_URL, API_ROUTES } from '@/libraries/api';

export default function CreateAdminPage() {
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    username: '',
    password: '',
    dob: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_BASE_URL}${API_ROUTES.CREATE_ADMIN}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to create admin');
      }

      // Handle successful creation (e.g., show success message, reset form)
      console.log('Admin created successfully');
      setFormData({ first_name: '', last_name: '', username: '', password: '', dob: '' });
    } catch (error) {
      console.error('Error creating admin:', error);
      // Handle error (e.g., show error message)
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen">
      <div className="w-full max-w-md">
        <h1 className="text-3xl font-bold mb-8 text-center">Create Admin</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="First Name"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            required
          />
          <Input
            label="Last Name"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            required
          />
          <Input
            label="Username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
          <Input
            label="Password"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
          <Input
            label="Date of Birth"
            name="dob"
            type="date"
            value={formData.dob}
            onChange={handleChange}
            required
          />
          <Button type="submit" color="primary" className="w-full">
            Create Admin
          </Button>
        </form>
      </div>
    </div>
  );
}