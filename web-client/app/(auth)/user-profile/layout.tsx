import MenuSideBar from "@/components/menu_side_bar";
import { IMenuSideBarItem } from "@/interface/UI/IMenuSideBar";
import { Bell, Clock, CreditCard, User } from "lucide-react";

const listMenuSideBar: IMenuSideBarItem[] = [
  {
    prefix: <User size={18} />,
    name: "Personal info",
    endpoint: "personal-info",
  },
  {
    prefix: <Clock size={18} />,
    name: "Login and security",
    endpoint: "login-and-security",
  },
  {
    prefix: <CreditCard size={18} />,
    name: "My payments",
    endpoint: "my-payments",
  },
  {
    prefix: <Bell size={18} />,
    name: "My orders",
    endpoint: "my-orders",
  },
];

export default function UserProfileLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <section className="flex mx-40 my-20">
      <nav className="mr-auto h-1/2">
        <MenuSideBar listTabs={listMenuSideBar} parentEndPoint="user-profile" />
      </nav>

      <div className="w-3/4">{children}</div>
    </section>
  );
}
