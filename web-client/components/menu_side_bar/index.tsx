"use client";
import { IMenuSideBar } from "@/interface/IMenuSideBar";
import { usePathname, useRouter } from "next/navigation";

const MenuSideBar: React.FC<IMenuSideBar> = ({ listTabs, parentEndPoint }) => {
  const pathname = usePathname();
  const router = useRouter();

  const handleTabClick = (endpoint: string) => {
    router.replace(`/${parentEndPoint}/${endpoint}`);
  };

  console.log(pathname);

  return (
    <div className="rounded-lg px-10 pt-10 border-2 shadow-lg h-full">
      {listTabs.map((item, index) => (
        <div
          className={`flex gap-2 mb-8 items-center cursor-pointer ${
            pathname === `/${parentEndPoint}/${item.endpoint}`
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
