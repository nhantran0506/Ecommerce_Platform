"use client";

import { useState, FormEvent } from "react";
import Link from "next/link";
import Image from "next/image";
import { usePathname, useRouter } from "next/navigation";
import loginImage from "@/assets/login-image.jpg";
import googleIcon from "@/assets/google-icon.png";
import zaloIcon from "@/assets/zalo-icon.png";
import facebookIcon from "@/assets/facebook-icon.png";
import { useGoogleAuth } from "@/hooks/useGoogleAuth";
import authAPIs from "@/api/auth";
import PasswordInput from "@/components/password_input";
import { Input } from "@nextui-org/react";
import { useTranslations } from "use-intl";
import { IReqLogin } from "@/api/auth/interface";

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();
  const pathname = usePathname();
  const locale = pathname.split("/")[1];
  const { handleGoogleLogin } = useGoogleAuth();
  const t = useTranslations();

  const handleUsernameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUsername(e.target.value);
  };

  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPassword(e.target.value);
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault();
    setError("");

    const reqBody: IReqLogin = {
      user_name: username,
      password: password,
    };

    try {
      const response = await authAPIs.login(reqBody);

      await localStorage.setItem("token", response.token);

      router.push("/");
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Invalid credentials. Please try again."
      );
    }
  };

  const handleGoogleLoginClick = async () => {
    try {
      setIsLoading(true);
      setError("");
      await handleGoogleLogin();
    } catch (error) {
      console.error("Google login error:", error);
      setError(
        error instanceof Error ? error.message : "Error with Google login"
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh)] flex">
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
          <h2 className="text-3xl font-bold text-gray-900 mb-8">
            {t("auth_welcome_back")}
          </h2>
          {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
          <form className="space-y-5" onSubmit={handleSubmit}>
            <Input
              id="username"
              name="username"
              type="text"
              required
              placeholder="Type your e-mail"
              value={username}
              onChange={handleUsernameChange}
              className="mb-2"
              fullWidth
            />

            <PasswordInput
              id="password"
              name="password"
              required
              // className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="Type your password"
              value={password}
              onChange={handlePasswordChange}
            />

            <div className="flex items-center justify-end">
              <Link
                href={`/${locale}/forgot-password`}
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
          {/* <div className="mt-6">
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
          </div> */}
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              {"Don't have an account? "}
              <Link
                href={`/${locale}/sign-up`}
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
