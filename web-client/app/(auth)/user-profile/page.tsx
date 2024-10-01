"use client";
import { IMenuSideBar } from "@/interface/User/IProfile";
import { User, Lock, CreditCard, Bell } from "react-feather";
import PersonalInfomationPage from "./personal-info";
import { ReactNode, useState } from "react";

const UserProfilePage = () => {
  const [activePageIndex, setActivePageIndex] = useState<number>(0);

  const listMenuSideBar: IMenuSideBar[] = [
    {
      prefix: <User size={18} />,
      name: "Personal info",
      child: <PersonalInfomationPage />,
    },
    {
      prefix: <Lock size={18} />,
      name: "Login and security",
      child: <div>Login and security content</div>,
    },
    {
      prefix: <CreditCard size={18} />,
      name: "My payments",
      child: <div>My payments</div>,
    },
    {
      prefix: <Bell size={18} />,
      name: "My orders",
      child: <div>My orders</div>,
    },
  ];

  const MenuSideBar = () => (
    <div className="rounded-lg px-8 pt-10 pb-2 border-2 shadow-md">
      {listMenuSideBar.map((item, index) => (
        <div
          className={`flex gap-2 mb-8 items-center ${
            activePageIndex == index ? "text-black" : "text-gray-400"
          }`}
          key={index}
          onClick={() => setActivePageIndex(index)}
        >
          {item.prefix}
          <p className={`font-semibold`}>{item.name}</p>
        </div>
      ))}
    </div>
  );

  return (
    <div className="flex mx-64 my-20">
      <div className="mr-auto">
        <MenuSideBar />
      </div>

      {/* Render a page base on menu */}
      <div className="w-2/3">{listMenuSideBar[activePageIndex].child}</div>
    </div>
  );
};

export default UserProfilePage;
