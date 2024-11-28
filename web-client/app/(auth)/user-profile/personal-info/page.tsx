"use client";
import authAPIs from "@/api/auth";
import SectionHeader from "@/components/section_header";
import { Button, Input } from "@nextui-org/react";
import { useEffect, useState } from "react";
import { X } from "react-feather";

const PersonalInfomationPage = () => {
  const [loading, setLoading] = useState(false);
  const [user, setUser] = useState<IResGetUser | null>(null); // Initial state as null

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
      label: "First name",
      placeholder: "Enter your first name",
      value: user?.first_name || "",
      field: "first_name",
    },
    {
      type: "text",
      label: "Last name",
      placeholder: "Enter your last name",
      value: user?.last_name || "",
      field: "last_name",
    },
    {
      type: "text",
      label: "Phone",
      placeholder: "Phone number",
      value: user?.phone_number || "",
      field: "phone_number",
    },
    {
      type: "email",
      label: "Email",
      placeholder: "Example@email.com",
      value: user?.email || "",
      field: "email",
    },
    {
      type: "text",
      label: "Address",
      placeholder: "Enter your full address",
      value: user?.address || "",
      field: "address",
    },
    {
      type: "date",
      label: "Date of Birth",
      placeholder: "Enter your date of birth",
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

  return (
    <SectionHeader
      title={"Personal Information"}
      // action={
      //   <Button variant="bordered" radius="full" className="font-bold">
      //     View profile
      //   </Button>
      // }
      content={
        <div>
          {loading ? (
            <div>Loading...</div>
          ) : (
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
          )}

          <div className="flex gap-4">
            <Button
              variant="solid"
              radius="full"
              className="text-white bg-black"
              onClick={() => handleUpdateUser()}
            >
              Update profile
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
              <div>Clear all</div>
            </Button>
          </div>
        </div>
      }
    />
  );
};

export default PersonalInfomationPage;
