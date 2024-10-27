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
    confirmPassword: '',
    dob: '',
  });
  const [notification, setNotification] = useState({ type: '', message: '' });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      setNotification({ type: 'error', message: 'Passwords do not match' });
      return;
    }
    try {
      const response = await fetch(`${API_BASE_URL}${API_ROUTES.CREATE_ADMIN}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({
          first_name: formData.first_name,
          last_name: formData.last_name,
          username: formData.username,
          password: formData.password,
          dob: formData.dob,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to create admin');
      }

      setNotification({ type: 'success', message: 'User has been created successfully' });
      setFormData({ first_name: '', last_name: '', username: '', password: '', confirmPassword: '', dob: '' });
    } catch (error) {
      setNotification({ type: 'error', message: 'There is an error happened' });
    }
  };

  return (
    <div className="w-full max-w-md mx-auto">
      <h1 className="text-3xl font-bold mb-8 text-center">Create Admin</h1>
      {notification.message && (
        <div className={`p-4 mb-4 rounded-md ${notification.type === 'success' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
          {notification.message}
        </div>
      )}
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
          label="Confirm Password"
          name="confirmPassword"
          type="password"
          value={formData.confirmPassword}
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
  );
}
