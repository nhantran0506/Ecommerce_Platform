'use client';

import { useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { API_BASE_URL, API_ROUTES } from '@/libraries/api';

export function useGoogleAuth() {
  const router = useRouter();

  const handleGoogleLogin = useCallback(async () => {
    try {
      // Fetch Google login URL from the back-end
      const response = await fetch(`${API_BASE_URL}${API_ROUTES.GET_GOOGLE_LOGIN}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include', // Include cookies
      });

      if (!response.ok) {
        throw new Error('Failed to get Google login URL');
      }

      const data = await response.json();

      // Open a popup window for Google login
      const width = 500;
      const height = 600;
      const left = window.screenX + (window.outerWidth - width) / 2;
      const top = window.screenY + (window.outerHeight - height) / 2;

      const popup = window.open(
        data.url,
        'GoogleAuth',
        `width=${width},height=${height},left=${left},top=${top},resizable=yes,scrollbars=yes`
      );

      if (!popup) {
        throw new Error('Popup blocked');
      }

      // Listen for messages from the popup
      return new Promise((resolve, reject) => {
        const handleMessage = (event: MessageEvent) => {
          // Log the event for debugging purposes
          console.log('Received message:', event);

          // Validate the event origin for security
          if (event.origin !== API_BASE_URL) {
            console.warn('Ignoring message from unknown origin:', event.origin);
            return;
          }

          // Handle success or error messages
          if (event.data && event.data.type === 'google-auth-success') {
            try {
              const token = event.data.token;
              if (token) {
                window.removeEventListener('message', handleMessage);
                localStorage.setItem('token', token); // Save the token
                resolve(token);
                router.push('/'); // Redirect on success
              }
            } catch (error) {
              console.error('Failed to handle token:', error);
              reject(error);
            }
          } else if (event.data && event.data.type === 'google-auth-error') {
            window.removeEventListener('message', handleMessage);
            reject(new Error(event.data.error || 'Authentication failed'));
          }
        };

        // Attach the event listener
        window.addEventListener('message', handleMessage);

        // Cleanup on timeout
        setTimeout(() => {
          window.removeEventListener('message', handleMessage);
          reject(new Error('Login timeout'));
        }, 300000); // 5 minutes timeout
      });

    } catch (error) {
      console.error('Google Login Error:', error);
      throw error;
    }
  }, [router]);

  return { handleGoogleLogin };
}
