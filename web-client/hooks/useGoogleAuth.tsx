'use client';

import { useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { API_BASE_URL, API_ROUTES } from '@/libraries/api';

export function useGoogleAuth() {
  const router = useRouter();

  const handleGoogleLogin = useCallback(async () => {
    try {
      console.log('Starting Google login process...'); // Debug log
      
      const response = await fetch(`${API_BASE_URL}${API_ROUTES.GET_GOOGLE_LOGIN}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include'
      });

      if (!response.ok) {
        throw new Error('Failed to get Google login URL');
      }

      const data = await response.json();
      console.log('Received Google login URL:', data.url); // Debug log
      
      const width = 500;
      const height = 600;
      const left = window.screenX + (window.outerWidth - width) / 2;
      const top = window.screenY + (window.outerHeight - height) / 2;
      
      console.log('Opening popup...'); // Debug log
      const popup = window.open(
        data.url,
        'Google Login',
        `width=${width},height=${height},left=${left},top=${top}`
      );

      if (!popup) {
        throw new Error('Popup blocked');
      }

      console.log('Popup opened, setting up message listener...'); // Debug log

      return new Promise((resolve, reject) => {
        const handleMessage = (event: MessageEvent) => {
          console.log('Received message event:', event); // Debug log
          console.log('Message data:', event.data); // Debug log

          const { type, data, error } = event.data || {};
          console.log('Parsed message:', { type, data, error }); // Debug log

          if (type === 'google-auth-success' && data) {
            console.log('Login successful, storing token...'); // Debug log
            window.removeEventListener('message', handleMessage);
            localStorage.setItem('token', data);
            console.log('Token stored, redirecting...'); // Debug log
            resolve(data);
            router.push('/');
          } else if (type === 'google-auth-error') {
            console.log('Login error received:', error); // Debug log
            window.removeEventListener('message', handleMessage);
            reject(new Error(error || 'Unknown error'));
          }
        };

        console.log('Adding message event listener...'); // Debug log
        window.addEventListener('message', handleMessage);

        // Add timeout
        setTimeout(() => {
          console.log('Login timeout reached'); // Debug log
          window.removeEventListener('message', handleMessage);
          reject(new Error('Login timeout'));
        }, 300000);
      });

    } catch (error) {
      console.error('Google Login Error:', error);
      throw error;
    }
  }, [router]);

  return { handleGoogleLogin };
}
