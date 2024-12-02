"use client";

import { usePathname, useRouter } from "next/navigation";

const UserProfilePage = () => {
  const router = useRouter();
  const pathname = usePathname();
  const locale = pathname.split("/")[1];

  router.push(`/${locale}/user-profile/personal-info`);

  return <></>;
};

export default UserProfilePage;
