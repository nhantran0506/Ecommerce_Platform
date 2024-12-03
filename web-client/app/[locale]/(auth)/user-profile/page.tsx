"use client";

import { usePathname, useRouter } from "next/navigation";
import { useEffect } from "react";

const UserProfilePage = () => {
  const router = useRouter();
  const pathname = usePathname();
  const locale = pathname.split("/")[1];

  useEffect(() => {
    router.push(`/${locale}/user-profile/personal-info`);
  }, [router, locale]);

  return <></>;
};

export default UserProfilePage;
