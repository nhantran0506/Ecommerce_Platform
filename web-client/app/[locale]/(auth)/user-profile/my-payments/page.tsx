import { Loader } from "lucide-react";
import { useTranslations } from "next-intl";

const MyPaymentPage = () => {
  const t = useTranslations();

  return (
    <div className="w-full h-full flex items-center justify-center gap-2">
      <span>{t("feature_development")}</span>
      <Loader />
    </div>
  );
};

export default MyPaymentPage;
