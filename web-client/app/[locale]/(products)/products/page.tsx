"use client";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import SingleComboBoxItem from "@/components/single_combo_box_item";
import {
  IFilterMenu,
  IOptionMenuFilter,
} from "@/interface/UI/ISingleComboBoxItem";
import ProductCard from "@/components/product_card";
import SearchBar from "@/components/search";
import SectionHeader from "@/components/section_header";
import { DollarSign, MapPin } from "react-feather";
import FilterMenu from "@/components/filter_menu";
import { Suspense, useEffect, useState } from "react";
import { productState } from "@/state/state";
import productAPIs from "@/api/product";
import { useTranslations } from "next-intl";
import ListProductCardSkeleton from "@/components/list_product_card_skeleton";

const ProductPage = () => {
  const router = useRouter();
  const pathname = usePathname();
  const locale = pathname.split("/")[1];

  const searchParams = useSearchParams();
  const [loading, setLoading] = useState(false);
  const productlist = productState((state) => state.productList);
  const setProductList = productState((state) => state.setProductList);
  const t = useTranslations();

  const searchQuery = searchParams.get("search") || "";

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);

        // Use recommended products API instead of getAll
        const res = searchQuery
          ? await productAPIs.getSearchListProduct(searchQuery)
          : await productAPIs.getRecommendedProducts();

        setProductList(res);
      } catch (error) {
        console.error("Failed to fetch products:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, [searchQuery, setProductList]);

  const listFilterOptionForPrice: IOptionMenuFilter[] = [
    { key: "ascending", label: "Ascending" },
    { key: "descending", label: "Descending" },
  ];

  const listFilterOptionForLocation: IOptionMenuFilter[] = [
    { key: "ha_noi", label: "Hà Nội" },
    { key: "tp_hcm", label: "Hồ Chí Minh" },
  ];

  const listFilterMenu: IFilterMenu[] = [
    {
      prefix: <MapPin size={28} />,
      listFilterOption: listFilterOptionForLocation,
    },
    {
      prefix: (
        <div className=" bg-black rounded-full p-2">
          <DollarSign size={18} color="white" />
        </div>
      ),
      listFilterOption: listFilterOptionForPrice,
    },
  ];

  return (
    <div className="px-72 my-8 w-full">
      <div className="flex gap-8">
        <FilterMenu />
        <div className="flex-1">
          <SectionHeader
            title={
              searchQuery
                ? `${t("products_search_result")} "${searchQuery}"`
                : t("products_all_product")
            }
            content={
              loading ? (
                <ListProductCardSkeleton gridCols={3} count={6} />
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                  {productlist?.map((item: IProductData, index: number) => (
                    <ProductCard
                      key={index}
                      product={item}
                      onClick={() =>
                        router.push(
                          "/" + locale + "/product/" + item.product_id
                        )
                      }
                    />
                  ))}
                </div>
              )
            }
          />
        </div>
      </div>
    </div>
  );
};

export default ProductPage;
