"use client";
import SectionHeader from "@/components/section_header";
import { useState, FormEvent } from "react";
import { Button, Input } from "@nextui-org/react";
import { X } from "react-feather";
import { API_BASE_URL, API_ROUTES } from "@/libraries/api";
import PasswordInput from "@/components/password_input";
import { useTranslations } from "next-intl";

const LoginAndSecurityPage = () => {
  const [formData, setFormData] = useState({
    old_password: "",
    new_password: "",
    confirm_password: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const t = useTranslations();

  const listFormInput: IInputItem[] = [
    {
      type: "password",
      label: t("input_current_password"),
      placeholder: t("placefolder_password"),
      value: formData.old_password,
      // name: "old_password",
    },
    {
      type: "password",
      label: t("input_current_password"),
      placeholder: t("placefolder_password"),
      value: formData.new_password,
      // name: "new_password",
    },
    {
      type: "password",
      label: t("input_confirm_password"),
      placeholder: t("placefolder_password"),
      value: formData.confirm_password,
      // name: "confirm_password",
    },
  ];

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const clearForm = () => {
    setFormData({
      old_password: "",
      new_password: "",
      confirm_password: "",
    });
    setError("");
    setSuccess("");
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    // Validate form data
    if (!formData.old_password || !formData.new_password) {
      setError("Both old and new passwords are required.");
      return;
    }

    if (formData.new_password !== formData.confirm_password) {
      setError("New password and confirmation do not match.");
      return;
    }

    try {
      const response = await fetch(
        `${API_BASE_URL}${API_ROUTES.CHANGE_PASSWORD}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify({
            old_password: formData.old_password,
            new_password: formData.new_password,
          }),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || "Failed to change password");
      }

      setSuccess("Password changed successfully");
      clearForm();
    } catch (error) {
      setError(
        "Failed to change password. Please check your current password and try again."
      );
    }
  };

  return (
    <SectionHeader
      title={t("user_profile_login_security_title")}
      content={
        <>
          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-2 gap-4">
              {listFormInput.map((item, index) => (
                <div
                  key={index}
                  className={`mb-4 ${
                    listFormInput.length % 2 !== 0 && index === 0
                      ? "col-span-2"
                      : ""
                  }`}
                >
                  <PasswordInput
                    label={item.label}
                    labelPlacement={"outside"}
                    placeholder={item.placeholder}
                    value={(item.value ?? "").toString()}
                    name={item.label}
                    onChange={handleChange}
                    isClearable
                    className="font-bold"
                  />
                </div>
              ))}
            </div>

            {error && <div className="text-red-500 text-sm mt-2">{error}</div>}
            {success && (
              <div className="text-green-500 text-sm mt-2">{success}</div>
            )}

            <div className="flex gap-4 mt-4">
              <Button
                type="submit"
                variant="solid"
                radius="full"
                className="text-white bg-black font-bold"
              >
                {t("btn_submit")}
              </Button>
              <Button variant="light" radius="full" onClick={clearForm}>
                <X size={15} />
                <div>{t("btn_clear")}</div>
              </Button>
            </div>
          </form>
        </>
      }
    />
  );
};

export default LoginAndSecurityPage;
