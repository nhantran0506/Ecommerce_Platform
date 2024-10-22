"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

const UserProfilePage = () => {
  const router = useRouter();

  useEffect(() => {
    router.push("/user-profile/personal-info");
  }, [router]);

  return <div>Redirecting to User Profile...</div>;
};

export default UserProfilePage;
