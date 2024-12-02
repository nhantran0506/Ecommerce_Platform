"use client";

import { useState, FormEvent, useEffect } from "react";
import { usePathname, useRouter } from "next/navigation";
import { API_BASE_URL, API_ROUTES } from "@/libraries/api";
import PasswordInput from "@/components/password_input";
import SectionHeader from "@/components/section_header";
import { Button } from "@nextui-org/react";
import { X } from "react-feather";

export default function ChangePasswordPage() {
  const [formData, setFormData] = useState({
    new_password: "",
    confirm_password: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const router = useRouter();
  const pathname = usePathname();
  const locale = pathname.split("/")[1];

  const [email, setEmail] = useState<string | null>(null);
  const [tempCode, setTempCode] = useState<string | null>(null);

  useEffect(() => {
    const userEmail = localStorage.getItem("userEmail");
    const userTempCode = localStorage.getItem("tempCode");

    setEmail(userEmail);
    setTempCode(userTempCode);

    if (!userEmail || !userTempCode) {
      setError("Missing email or temporary code.");
    }
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const clearForm = () => {
    setFormData({
      new_password: "",
      confirm_password: "",
    });
    setError("");
    setSuccess(false);
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess(false);

    if (!email || !tempCode) {
      setError("Missing email or temporary code.");
      return;
    }

    if (formData.new_password !== formData.confirm_password) {
      setError("New password and confirmation do not match.");
      return;
    }

    try {
      const response = await fetch(
        `${API_BASE_URL}${
          API_ROUTES.CHANGE_PASSWORD_WITH_CODE
        }?temp_code=${encodeURIComponent(
          tempCode
        )}&user_email=${encodeURIComponent(email)}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            new_password: formData.new_password,
          }),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Failed to change password");
      }

      setSuccess(true);
      clearForm();
      setTimeout(() => {
        router.push(`/${locale}/login`);
      }, 3000);
    } catch (error) {
      setError("Failed to change password. Please try again.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <SectionHeader
        title={"Change Password"}
        content={
          <>
            <form onSubmit={handleSubmit}>
              <div className="grid grid-cols-1 gap-4">
                <div className="mb-4">
                  <PasswordInput
                    label="New Password"
                    placeholder="Enter your new password"
                    value={formData.new_password}
                    name="new_password"
                    onChange={handleChange}
                    isClearable
                    className="font-bold"
                  />
                </div>
                <div className="mb-4">
                  <PasswordInput
                    label="Confirm New Password"
                    placeholder="Confirm your new password"
                    value={formData.confirm_password}
                    name="confirm_password"
                    onChange={handleChange}
                    isClearable
                    className="font-bold"
                  />
                </div>
              </div>

              {error && (
                <div className="text-red-500 text-sm mt-2">{error}</div>
              )}
              {success && (
                <div className="text-green-500 text-sm mt-2">
                  Password changed successfully.
                </div>
              )}

              <div className="flex gap-4 mt-4">
                <Button
                  type="submit"
                  variant="solid"
                  radius="full"
                  className="text-white bg-black"
                >
                  Change Password
                </Button>
                <Button variant="light" radius="full" onClick={clearForm}>
                  <X size={15} />
                  <div>Clear all</div>
                </Button>
              </div>
            </form>
          </>
        }
      />
    </div>
  );
}
