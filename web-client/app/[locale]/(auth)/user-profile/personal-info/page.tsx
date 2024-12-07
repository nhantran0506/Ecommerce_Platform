"use client";
import authAPIs from "@/api/auth";
import { IReqUpdateUser, IResGetUser } from "@/api/auth/interface";
import PersonalInfoSkeleton from "@/components/personal-info-skeleton";
import SectionHeader from "@/components/section_header";
import { Button, Input } from "@nextui-org/react";
import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { X } from "react-feather";

const PersonalInfomationPage = () => {
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState<IResGetUser | null>(null);
  const t = useTranslations();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        setLoading(true);
        const res = await authAPIs.getCurrentUser();
        setUser(res);
      } catch (error) {
        console.error("Failed to fetch user:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []);

  const handleInputChange = (field: keyof IResGetUser, value: string) => {
    if (user) {
      setUser((prevUser) => ({
        ...prevUser!,
        [field]: value,
      }));
    }
  };

  const listFormInput: {
    type: string;
    label: string;
    placeholder: string;
    value: string;
    field: keyof IResGetUser;
  }[] = [
    {
      type: "text",
      label: t("input_first_name"),
      placeholder: t("placeholder_first_name"),
      value: user?.first_name || "",
      field: "first_name",
    },
    {
      type: "text",
      label: t("input_last_name"),
      placeholder: t("placeholder_last_name"),
      value: user?.last_name || "",
      field: "last_name",
    },
    {
      type: "text",
      label: t("input_phone"),
      placeholder: t("placeholder_phone"),
      value: user?.phone_number || "",
      field: "phone_number",
    },
    {
      type: "email",
      label: t("input_email"),
      placeholder: t("placeholder_email"),
      value: user?.email || "",
      field: "email",
    },
    {
      type: "text",
      label: t("input_address"),
      placeholder: t("placeholder_address"),
      value: user?.address || "",
      field: "address",
    },
    {
      type: "date",
      label: t("input_dob"),
      placeholder: "",
      value: user?.dob || "",
      field: "dob",
    },
  ];

  const handleUpdateUser = async () => {
    try {
      setLoading(true);
      const reqBody: IReqUpdateUser = {
        first_name: user?.first_name ?? "",
        last_name: user?.last_name ?? "",
        address: user?.address ?? "",
        dob: user?.dob ?? "",
      };

      await authAPIs.updateCurrentUser(reqBody);
    } catch (error) {
      console.error("Failed to fetch user:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <PersonalInfoSkeleton />;
  }

  return (
    <SectionHeader
      title={t("user_profile_personal_info_title")}
      // action={
      //   <Button variant="bordered" radius="full" className="font-bold">
      //     View profile
      //   </Button>
      // }
      content={
        <div>
          <div className="grid grid-cols-2 gap-4">
            {listFormInput.map((item, index) => (
              <div
                key={index}
                className={`mb-4 ${
                  listFormInput.length % 2 !== 0 &&
                  index === listFormInput.length - 1
                    ? "col-span-2"
                    : ""
                }`}
              >
                <Input
                  type={item.type}
                  label={item.label}
                  labelPlacement="outside"
                  placeholder={item.placeholder}
                  isClearable
                  className="font-bold"
                  value={item.value}
                  onChange={(e) =>
                    handleInputChange(item.field, e.target.value)
                  }
                  onClear={() => handleInputChange(item.field, "")}
                />
              </div>
            ))}
          </div>

          <div className="flex gap-4">
            <Button
              variant="solid"
              radius="full"
              className="text-white bg-black font-bold"
              onClick={() => handleUpdateUser()}
            >
              {t("btn_submit")}
            </Button>
            <Button
              variant="light"
              radius="full"
              onClick={() =>
                setUser({
                  user_id: "",
                  phone_number: "",
                  dob: "",
                  role: "",
                  first_name: "",
                  last_name: "",
                  address: "",
                  email: "",
                })
              }
            >
              <X size={15} />
              <div>{t("btn_clear")}</div>
            </Button>
          </div>
        </div>
      }
    />
  );
};

export default PersonalInfomationPage;
