"use client";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import {
  IFilterMenu,
  IOptionMenuFilter,
} from "@/interface/UI/ISingleComboBoxItem";
import ProductCard from "@/components/product_card";
import SectionHeader from "@/components/section_header";
import { DollarSign, MapPin } from "react-feather";
import FilterMenu from "@/components/filter_menu";
import { useEffect, useState } from "react";
import { useCategporyState, useProductState } from "@/state/state";
import productAPIs from "@/api/product";
import { useTranslations } from "next-intl";
import ListProductCardSkeleton from "@/components/list_product_card_skeleton";

const ProductPage = () => {
  const router = useRouter();
  const pathname = usePathname();
  const t = useTranslations();
  const searchParams = useSearchParams();
  const [loading, setLoading] = useState(false);
  const [isHydrated, setIsHydrated] = useState(false);

  const productlist = useProductState((state) => state.productList);
  const setProductList = useProductState((state) => state.setProductList);
  const cateList = useCategporyState((state) => state.categoryList);
  const setCateList = useCategporyState((state) => state.setCategoryList);

  const locale = pathname.split("/")[1];
  const searchQuery = searchParams.get("search") || "";

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        console.log("productlist.length ", productlist.length);

        setLoading(true);
        if (searchQuery) {
          const products = await productAPIs.getSearchListProduct(searchQuery);
          setProductList(products);
        } else if (isHydrated && productlist.length === 0) {
          const products = await productAPIs.getAll();
          setProductList(products);
        }

        if (isHydrated && cateList.length === 0) {
          const cateListRes = await productAPIs.getAllCategories();
          setCateList(cateListRes);
        }
      } catch (error) {
        console.error("Failed to fetch products:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, [searchQuery, setProductList, isHydrated]);

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
                <div className="grid grid-cols-3 gap-8">
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
