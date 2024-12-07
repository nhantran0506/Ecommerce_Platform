"use client";
import { useEffect, useState } from "react";
import { Button, Input, Textarea } from "@nextui-org/react";
import { useTranslations } from "next-intl";
import { X } from "react-feather";
import SectionHeader from "@/components/section_header";
import PersonalInfoSkeleton from "@/components/personal-info-skeleton";
import shopAPIs from "@/api/shop";

interface IShopInfo {
  shop_name: string;
  shop_address: string;
  shop_phone_number: string;
  shop_bio: string;
}

const ShopProfilePage = () => {
  const [loading, setLoading] = useState(false);
  const [shop, setShop] = useState<IShopInfo | null>(null);
  const [haveShop, setHaveShop] = useState<boolean>(false);
  const t = useTranslations();

  useEffect(() => {
    const fetchShopInfo = async () => {
      try {
        setLoading(true);
        const res = await shopAPIs.getCurrentShopInfo();

        const shopInfo: IShopInfo = {
          shop_name: res.shop_name,
          shop_address: res.shop_address,
          shop_phone_number: res.shop_phone_number,
          shop_bio: res.shop_bio,
        };

        setShop(shopInfo);
        setHaveShop(true);
      } catch (error) {
        console.error("Failed to fetch shop info:", error);
        setHaveShop(false);
      } finally {
        setLoading(false);
      }
    };

    fetchShopInfo();
  }, []);

  const handleInputChange = (field: keyof IShopInfo, value: string) => {
    if (shop) {
      setShop((prevShop) => ({
        ...prevShop!,
        [field]: value,
      }));
    }
  };

  const listFormInput = [
    {
      type: "text",
      label: t("input_shop_name"),
      placeholder: t("placeholder_shop_name"),
      value: shop?.shop_name || "",
      field: "shop_name" as keyof IShopInfo,
    },
    {
      type: "text",
      label: t("input_shop_address"),
      placeholder: t("placeholder_shop_address"),
      value: shop?.shop_address || "",
      field: "shop_address" as keyof IShopInfo,
    },
    {
      type: "text",
      label: t("input_shop_phone"),
      placeholder: t("placeholder_shop_phone"),
      value: shop?.shop_phone_number || "",
      field: "shop_phone_number" as keyof IShopInfo,
    },
  ];

  const handleUpdateShop = async () => {
    if (!haveShop) {
      // create shop
      try {
        setLoading(true);
        await shopAPIs.createShop({
          shop_name: shop?.shop_name ?? "",
          shop_address: shop?.shop_address ?? "",
          shop_bio: shop?.shop_bio ?? "",
        });
      } catch (error) {
        console.error("Failed to update shop:", error);
      } finally {
        setLoading(false);
      }
    } else {
      // update shop
    }
  };

  if (loading) {
    return <PersonalInfoSkeleton />;
  }

  return (
    <SectionHeader
      title={t("shop_profile_title")}
      content={
        <div>
          <div className="grid grid-cols-2 gap-4">
            {listFormInput.map((item, index) => (
              <div
                key={index}
                className={`mb-4 ${
                  listFormInput.length % 2 !== 0 &&
                  index === listFormInput.length - 1
                    ? "col-span-2"
                    : ""
                }`}
              >
                <Input
                  type={item.type}
                  label={item.label}
                  labelPlacement="outside"
                  placeholder={item.placeholder}
                  isClearable
                  className="font-bold"
                  value={item.value}
                  onChange={(e) =>
                    handleInputChange(item.field, e.target.value)
                  }
                  onClear={() => handleInputChange(item.field, "")}
                />
              </div>
            ))}
            <div className="col-span-2">
              <Textarea
                label={t("input_shop_bio")}
                labelPlacement="outside"
                placeholder={t("placeholder_shop_bio")}
                value={shop?.shop_bio || ""}
                onChange={(e) => handleInputChange("shop_bio", e.target.value)}
                className="font-bold"
              />
            </div>
          </div>

          <div className="flex gap-4 mt-4">
            <Button
              variant="solid"
              radius="full"
              className="text-white bg-black font-bold"
              onClick={handleUpdateShop}
            >
              {t("btn_submit")}
            </Button>
            <Button
              variant="light"
              radius="full"
              onClick={() =>
                setShop({
                  shop_name: "",
                  shop_address: "",
                  shop_phone_number: "",
                  shop_bio: "",
                })
              }
            >
              <X size={15} />
              <div>{t("btn_clear")}</div>
            </Button>
          </div>
        </div>
      }
    />
  );
};

export default ShopProfilePage;
