import MenuSideBar from "@/components/menu_side_bar";
import { IMenuSideBarItem } from "@/interface/UI/IMenuSideBar";
import { Database, Grid, ShoppingCart, Store } from "lucide-react";
import { useTranslations } from "next-intl";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const t = useTranslations();

  const listMenuSideBar: IMenuSideBarItem[] = [
    {
      prefix: <Store size={18} />,
      name: t("shop_profile"),
      endpoint: "shop-profile",
    },
    {
      prefix: <Database size={18} />,
      name: t("shop_dashboard"),
      endpoint: "dashboard",
    },
    {
      prefix: <Grid size={18} />,
      name: t("shop_products"),
      endpoint: "product-analyze",
    },
    {
      prefix: <ShoppingCart size={18} />,
      name: t("shop_orders"),
      endpoint: "order-analyze",
    },
  ];

  return (
    <section className="flex mx-40 my-20 ">
      <nav className="mr-auto">
        <MenuSideBar listTabs={listMenuSideBar} parentEndPoint="shop" />
      </nav>

      <div className="w-3/4">{children}</div>
    </section>
  );
}
