"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

const ShopPage = () => {
  const router = useRouter();

  useEffect(() => {
    router.push("/shop/dashboard");
  }, [router]);

  return <div>Redirecting to Dashboard...</div>;
};

export default ShopPage;
