import MenuSideBar from "@/components/menu_side_bar";
import { IMenuSideBarItem } from "@/interface/UI/IMenuSideBar";
import { Database, Grid, ShoppingCart } from "lucide-react";

const listMenuSideBar: IMenuSideBarItem[] = [
  {
    prefix: <Database size={18} />,
    name: "Dashboard",
    endpoint: "dashboard",
  },
  {
    prefix: <Grid size={18} />,
    name: "Product",
    endpoint: "product-analyze",
  },
  {
    prefix: <ShoppingCart size={18} />,
    name: "Orders",
    endpoint: "order-analyze",
  },
];

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <section className="flex mx-40 my-20 ">
      <nav className="mr-auto">
        <MenuSideBar listTabs={listMenuSideBar} parentEndPoint="shop" />
      </nav>

      <div className="w-3/4">{children}</div>
    </section>
  );
}
