import MenuSideBar from "@/components/menu_side_bar";
import { IMenuSideBarItem } from "@/interface/UI/IMenuSideBar";
import { Bell, Clock, CreditCard, User } from "lucide-react";
import { useTranslations } from "next-intl";

export default function UserProfileLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const t = useTranslations();

  const listMenuSideBar: IMenuSideBarItem[] = [
    {
      prefix: <User size={20} />,
      name: t("user_profile_personal_info_title"),
      endpoint: "personal-info",
    },
    {
      prefix: <Clock size={20} />,
      name: t("user_profile_login_security_title"),
      endpoint: "login-and-security",
    },
    {
      prefix: <CreditCard size={20} />,
      name: t("user_profile_payment_title"),
      endpoint: "my-payments",
    },
    {
      prefix: <Bell size={20} />,
      name: t("user_profile_order_title"),
      endpoint: "my-orders",
    },
  ];

  return (
    <section className="flex mx-40 my-20">
      <nav className="mr-auto h-1/2">
        <MenuSideBar listTabs={listMenuSideBar} parentEndPoint="user-profile" />
      </nav>

      <div className="w-[70%]">{children}</div>
    </section>
  );
}
