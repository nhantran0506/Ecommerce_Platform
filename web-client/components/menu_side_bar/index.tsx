"use client";
import { IMenuSideBar } from "@/interface/UI/IMenuSideBar";
import { usePathname, useRouter } from "next/navigation";

const MenuSideBar: React.FC<IMenuSideBar> = ({ listTabs, parentEndPoint }) => {
  const pathname = usePathname();
  const router = useRouter();
  const locale = pathname.split("/")[1];

  const handleTabClick = (endpoint: string) => {
    router.replace(`/${locale}/${parentEndPoint}/${endpoint}`);
  };

  console.log(pathname);

  return (
    <div className="rounded-lg px-10 pt-8 border-2 shadow-lg h-64">
      {listTabs.map((item, index) => (
        <div
          className={`flex gap-2 mb-8 items-center cursor-pointer ${
            pathname === `/${locale}/${parentEndPoint}/${item.endpoint}`
              ? "text-black"
              : "text-gray-400"
          }`}
          key={index}
          onClick={() => handleTabClick(item.endpoint)}
        >
          {item.prefix}
          <p className="font-semibold">{item.name}</p>
        </div>
      ))}
    </div>
  );
};

export default MenuSideBar;
