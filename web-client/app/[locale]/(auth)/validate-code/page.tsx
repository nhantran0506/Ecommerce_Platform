"use client";

import { useState, FormEvent, useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import { API_BASE_URL, API_ROUTES } from "@/libraries/api";

export default function ValidateCodePage() {
  const [code, setCode] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const router = useRouter();
  const pathname = usePathname();
  const locale = pathname.split("/")[1];
  const [email, setEmail] = useState<string | null>(null);
  const [canResend, setCanResend] = useState(false);
  const [countdown, setCountdown] = useState(60);

  useEffect(() => {
    setEmail(localStorage.getItem("userEmail"));
  }, []);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");
    setSuccess(false);

    try {
      const response = await fetch(
        `${API_BASE_URL}${API_ROUTES.PASSWORD_CODE_VALIDATE}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email, temp_code: code }),
        }
      );

      if (!response.ok) {
        throw new Error("Invalid code. Please try again.");
      }

      setSuccess(true);
      setTimeout(() => {
        router.push(`/${locale}/change-password`);
      }, 3000);
    } catch (error) {
      setError("Failed to validate code. Please try again.");
    }
  };

  const handleResendCode = async () => {
    if (!canResend) return; // Prevent sending if not allowed
    setCanResend(false);
    setCountdown(60); // Reset countdown

    try {
      const response = await fetch(
        `${API_BASE_URL}${API_ROUTES.FORGOT_PASSWORD}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ email }), // Use email from local storage
        }
      );

      if (!response.ok) {
        throw new Error("Failed to resend code. Please try again.");
      }

      // Optionally, show success message
      setSuccess(true);
    } catch (error) {
      setError("Failed to resend code. Please try again.");
    }
  };

  useEffect(() => {
    if (countdown > 0 && !canResend) {
      const timer = setInterval(() => {
        setCountdown((prev) => prev - 1);
      }, 1000);
      return () => clearInterval(timer);
    } else if (countdown === 0) {
      setCanResend(true);
    }
  }, [countdown, canResend]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Validate Code
        </h2>
        {error && <p className="text-center text-red-500 text-sm">{error}</p>}
        {success && (
          <p className="text-center text-green-500 text-sm">
            Code validated successfully.
          </p>
        )}
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div>
            <label htmlFor="code" className="sr-only">
              Verification Code
            </label>
            <input
              id="code"
              name="code"
              type="text"
              required
              className="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              placeholder="Enter 6-digit code"
              value={code}
              onChange={(e) => setCode(e.target.value)}
            />
          </div>
          <div>
            <button
              type="submit"
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-black hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
            >
              Validate Code
            </button>
          </div>
        </form>
        <button
          onClick={handleResendCode}
          disabled={!canResend}
          className={`group relative w-full flex justify-center py-1 px-2 border border-transparent text-sm font-medium rounded-md text-white ${
            canResend
              ? "bg-black hover:bg-gray-800"
              : "bg-gray-400 cursor-not-allowed"
          }`}
        >
          Resend Code {countdown > 0 && `(${countdown})`}
        </button>
      </div>
    </div>
  );
}
