"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

const UserProfilePage = () => {
  const router = useRouter();

  useEffect(() => {
    router.push("/user-profile/personal-info");
  }, []);

  return <></>;
};

export default UserProfilePage;
