"use client";

import { usePathname, useRouter } from "next/navigation";

const ShopPage = () => {
  const router = useRouter();
  const pathname = usePathname();
  const locale = pathname.split("/")[1];

  router.push(`/${locale}/shop/dashboard`);

  return <></>;
};

export default ShopPage;
