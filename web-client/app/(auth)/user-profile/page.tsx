"use client";
import { User, Lock, CreditCard, Bell } from "react-feather";
import PersonalInfomationPage from "./personal-info";
import { IMenuSideBarItem } from "@/interface/IMenuSideBar";
import MenuSideBar from "@/components/menu_side_bar";

const UserProfilePage = () => {
  const listMenuSideBar: IMenuSideBarItem[] = [
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

  return (
    <div className="flex mx-64 my-20">
      <MenuSideBar listTabs={listMenuSideBar} />
    </div>
  );
};

export default UserProfilePage;
