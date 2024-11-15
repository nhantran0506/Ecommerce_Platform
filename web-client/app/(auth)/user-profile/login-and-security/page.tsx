import SectionHeader from "@/components/section_header";
import { IInputItem } from "@/interface/UI/IProfile";
import { Button, Input } from "@nextui-org/react";
import { X } from "react-feather";

const LoginAndSecurityPage = () => {
  const listFormInput: IInputItem[] = [
    {
      type: "text",
      label: "Current password",
      placeholder: "Enter your current password",
    },
    {
      type: "text",
      label: "New password",
      placeholder: "Enter your new password",
    },
    {
      type: "text",
      label: "Confirm new password",
      placeholder: "Confirm your new password",
    },
  ];

  return (
    <SectionHeader
      title={"Login and Security"}
      content={
        <>
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

          <div className="flex gap-4">
            <Button
              variant="solid"
              radius="full"
              className="text-white bg-black"
            >
              Update password
            </Button>
            <Button variant="light" radius="full">
              <X size={15} />
              <div>Clear all</div>
            </Button>
          </div>
        </>
      }
    />
  );
};

export default LoginAndSecurityPage;
