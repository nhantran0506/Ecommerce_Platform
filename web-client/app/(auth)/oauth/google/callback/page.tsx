'use client';

import { useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import { API_BASE_URL, API_ROUTES } from '@/libraries/api';

export default function GoogleCallback() {
  const searchParams = useSearchParams();

  useEffect(() => {
    const handleCallback = async () => {
      try {
        // Get the code and state from URL parameters
        const code = searchParams.get('code');
        const state = searchParams.get('state');

        if (!code) {
          throw new Error('No authorization code received');
        }

        // Exchange the code for a token
        const response = await fetch(`${API_BASE_URL}${API_ROUTES.LOGIN_GOOGLE}?code=${code}&state=${state}`, {
          method: 'GET',
          credentials: 'include',
        });

        if (!response.ok) {
          throw new Error('Failed to exchange code for token');
        }

        const data = await response.json();
        
        // Send message to parent window
        if (window.opener) {
          window.opener.postMessage({
            type: 'google-auth-success',
            data: data.token
          }, window.location.origin);
        }
      } catch (error) {
        // Send error to parent window
        if (window.opener) {
          window.opener.postMessage({
            type: 'google-auth-error',
            error: error instanceof Error ? error.message : 'Authentication failed'
          }, window.location.origin);
        }
      }
    };

    handleCallback();
  }, [searchParams]);

  return (
    <div className="flex items-center justify-center min-h-screen">
      <p className="text-gray-600">Completing login, please wait...</p>
    </div>
  );
} 