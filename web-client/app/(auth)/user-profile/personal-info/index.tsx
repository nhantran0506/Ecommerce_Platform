"use client";
import SectionHeader from "@/components/section_header";
import { IProfileInput } from "@/interface/User/IProfile";
import { Button, Input } from "@nextui-org/react";
import { X } from "react-feather";

const PersonalInfomationPage = () => {
  const listFormInput: IProfileInput[] = [
    {
      type: "text",
      label: "First name",
      placeholder: "Enter your first name",
    },
    {
      type: "text",
      label: "Last name",
      placeholder: "Enter your last name",
    },
    {
      type: "text",
      label: "Phone",
      placeholder: "Phone number",
    },
    {
      type: "email",
      label: "Email",
      placeholder: "Example@email.com",
    },
    {
      type: "text",
      label: "Address",
      placeholder: "Enter your full address",
    },
  ];

  return (
    <div>
      <div className="flex justify-between">
        <h1 className="font-bold text-3xl mb-10">Personal info</h1>
        <Button variant="bordered" radius="full" className="font-bold">
          View profile
        </Button>
      </div>
      <div>
        <SectionHeader
          title="Account info"
          content={
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
                    labelPlacement={"outside"}
                    placeholder={item.placeholder}
                    isClearable
                    className="font-bold"
                  />
                </div>
              ))}
            </div>
          }
        />

        <div className="flex gap-4">
          <Button variant="solid" radius="full" className="text-white bg-black">
            Update profile
          </Button>
          <Button variant="light" radius="full">
            <X size={15} />
            <div>Clear all</div>
          </Button>
        </div>
      </div>
    </div>
  );
};

export default PersonalInfomationPage;
