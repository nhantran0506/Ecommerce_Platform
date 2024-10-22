"use client";
import SectionHeader from "@/components/section_header";
import { InputTypeEnum } from "@/constant/enum";
import { IInputItem } from "@/interface/UI/IProfile";
import { Button, Input } from "@nextui-org/react";
import { X } from "react-feather";

const PersonalInfomationPage = () => {
  const listFormInput: IInputItem[] = [
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
    <SectionHeader
      title={"Personal information"}
      action={
        <Button variant="bordered" radius="full" className="font-bold">
          View profile
        </Button>
      }
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
                  labelPlacement={"outside"}
                  placeholder={item.placeholder}
                  isClearable
                  className="font-bold"
                  // endContent={
                  //   item.label == "Price" ? (
                  //     <div className="pointer-events-none flex items-center">
                  //       <span className="text-default-400 text-small">
                  //         VND
                  //       </span>
                  //     </div>
                  //   ) : (
                  //     <></>
                  //   )
                  // }
                />
              </div>
            ))}
          </div>

          <div className="flex gap-4">
            <Button
              variant="solid"
              radius="full"
              className="text-white bg-black"
            >
              Update profile
            </Button>
            <Button variant="light" radius="full">
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
