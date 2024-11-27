"use client";

import { useState, FormEvent, useEffect } from "react";
import Link from "next/link";
import Image from "next/image";
import { useRouter, useSearchParams } from "next/navigation";
import { API_BASE_URL, API_ROUTES } from "@/libraries/api";
import loginImage from "@/assets/login-image.jpg";
import googleIcon from "@/assets/google-icon.png";
import zaloIcon from "@/assets/zalo-icon.png";
import facebookIcon from "@/assets/facebook-icon.png";
import { useGoogleAuth } from "@/hooks/useGoogleAuth";
import PasswordInput from "@/components/password_input";

export default function LoginPage() {
  const [form_data, set_form_data] = useState({
    user_name: "",
    password: "",
  });
  const [error, set_error] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  const { handleGoogleLogin } = useGoogleAuth();

  const handle_change = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    set_form_data((prev_state) => ({
      ...prev_state,
      [name]: value,
    }));
  };

  const handle_submit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    set_error("");

    try {
      const response = await fetch(`${API_BASE_URL}${API_ROUTES.LOGIN}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(form_data),
      });
      if (!response.ok) {
        throw new Error("Login failed");
      }
      if (response.status == 401) {
        throw new Error("Wrong password or username.");
      }

      const data = await response.json();
      localStorage.setItem("token", data.token);
      router.push("/");
    } catch (error) {
      set_error("Invalid username or password. Please try again.");
    }
  };

  const handleGoogleLoginClick = async () => {
    try {
      setIsLoading(true);
      set_error("");
      await handleGoogleLogin();
    } catch (error) {
      console.error("Google login error:", error);
      set_error(
        error instanceof Error ? error.message : "Error with Google login"
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(91vh)] flex">
      <div className="w-1/2 relative">
        <Image
          src={loginImage}
          alt="login-image"
          layout="fill"
          objectFit="cover"
        />
      </div>
      <div className="w-1/2 flex items-center justify-center bg-white">
        <div className="max-w-md w-full p-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back!
          </h2>
          {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
          <form className="space-y-4" onSubmit={handle_submit}>
            <div>
              <label
                htmlFor="user_name"
                className="block text-sm font-medium text-gray-700 mb-1"
              >
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
              <PasswordInput
                id="password"
                name="password"
                required
                className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="Type your password"
                value={form_data.password}
                onChange={handle_change}
              />
            </div>
            <div className="flex items-center justify-end">
              <Link
                href="/forgot-password"
                className="text-sm text-indigo-600 hover:text-indigo-500"
              >
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
            <p className="text-center text-sm text-gray-500">
              or do it via other accounts
            </p>
            <div className="mt-4 flex justify-center space-x-4">
              <button
                className="p-2 border border-gray-300 rounded-full relative"
                onClick={handleGoogleLoginClick}
                disabled={isLoading}
              >
                {isLoading ? (
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-5 h-5 border-t-2 border-gray-500 rounded-full animate-spin"></div>
                  </div>
                ) : (
                  <Image src={googleIcon} alt="Google" width={24} height={24} />
                )}
              </button>
              <button className="p-2 border border-gray-300 rounded-full">
                <Image src={zaloIcon} alt="Zalo" width={24} height={24} />
              </button>
              <button className="p-2 border border-gray-300 rounded-full">
                <Image
                  src={facebookIcon}
                  alt="Facebook"
                  width={24}
                  height={24}
                />
              </button>
            </div>
          </div>
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              {"Don't have an account? "}
              <Link
                href="/sign-up"
                className="font-medium text-indigo-600 hover:text-indigo-500"
              >
                Sign Up
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
