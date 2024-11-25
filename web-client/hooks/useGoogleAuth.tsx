'use client';

import { useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { API_BASE_URL, API_ROUTES } from '@/libraries/api';

export function useGoogleAuth() {
  const router = useRouter();

  // Handle the login process by calling the back-end to get the Google login URL
  const handleGoogleLogin = async () => {
    try {
      // Step 1: Request the Google login URL from the back-end
      const response = await fetch(`${API_BASE_URL}${API_ROUTES.GET_GOOGLE_LOGIN}`, {
        method: "GET",
        credentials: "include", // This ensures cookies (like access tokens) are sent with the request
      });

      if (!response.ok) {
        throw new Error("Failed to fetch Google login URL");
      }

      const data = await response.json();
      console.log(data);

      if (data?.url) {
        // Step 2: Redirect the user to the Google login URL
        window.location.href = data.url;
      } else {
        throw new Error("Google login URL not found in response");
      }
    } catch (error) {
      console.error("Error initiating Google login:", error);
      throw error;
    }
  };

  // Use this hook to call the protected API route after successful login
  const fetchProtectedData = useCallback(async () => {
    try {
      // Step 3: Make an authenticated request to the back-end (the access token will be sent automatically)
      const response = await fetch(`${API_BASE_URL}/protected-data`, {
        method: "GET",
        credentials: "include", // Ensures cookies are included with the request
      });

      if (!response.ok) {
        throw new Error("Failed to fetch protected data");
      }

      const data = await response.json();
      console.log("Protected data:", data);
      return data;
    } catch (error) {
      console.error("Error fetching protected data:", error);
      throw error;
    }
  }, []);

  return { handleGoogleLogin, fetchProtectedData };
}
