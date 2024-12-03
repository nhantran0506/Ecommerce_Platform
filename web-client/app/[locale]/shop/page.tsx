"use client";

import { usePathname, useRouter } from "next/navigation";
import { useEffect } from "react";

const ShopPage = () => {
  const router = useRouter();
  const pathname = usePathname();
  const locale = pathname.split("/")[1];

  useEffect(() => {
    router.push(`/${locale}/shop/dashboard`);
  }, [router, locale]);

  return <></>;
};

export default ShopPage;
