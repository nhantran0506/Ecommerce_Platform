import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { API_BASE_URL, API_ROUTES } from '@/libraries/api';

declare global {
  interface Window {
    gapi: any;
  }
}

export function useGoogleAuth() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadGoogleAuth = () => {
      if (!window.gapi) {
        console.error("Google API not loaded");
        setError("Google API not loaded");
        return;
      }

      window.gapi.load('auth2', () => {
        window.gapi.auth2.init({
          client_id: "62998154158-n74ummjoutr08agvknfkvkmf9lnvtog7.apps.googleusercontent.com",
        }).then(() => {
          console.log("Google Auth initialized successfully");
        }, (error: any) => {
          console.error("Error initializing Google Auth:", error);
          setError(`Failed to initialize Google Auth: ${error.error}`);
        });
      });
    };

    const script = document.createElement('script');
    script.src = 'https://apis.google.com/js/platform.js';
    script.async = true;
    script.defer = true;
    script.onload = loadGoogleAuth;
    script.onerror = () => {
      console.error("Failed to load Google platform script");
      setError("Failed to load Google authentication script");
    };
    document.body.appendChild(script);

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  const signIn = () => {
    if (!window.gapi) {
      console.error("Google API not loaded");
      setError("Google API not loaded");
      return;
    }

    const auth2 = window.gapi.auth2.getAuthInstance();
    auth2.signIn().then(
      (googleUser: any) => {
        const id_token = googleUser.getAuthResponse().id_token;
        console.log("Google sign-in successful, sending token to backend");
        fetch(`${API_BASE_URL}${API_ROUTES.GOOGLE_LOGIN}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ token: id_token }),
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
          })
          .then((data) => {
            console.log("Backend response:", data);
            localStorage.setItem("token", data.token);
            router.push('/');
          })
          .catch((error) => {
            console.error('Error:', error);
            setError(`Failed to authenticate with the server: ${error.message}`);
          });
      },
      (error: any) => {
        console.error('Google Sign-In Error: ', error);
        setError(`Failed to sign in with Google: ${error.error}`);
      }
    );
  };

  return { signIn, error };
}
