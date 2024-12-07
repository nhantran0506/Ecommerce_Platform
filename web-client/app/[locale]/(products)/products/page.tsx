"use client";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import ProductCard from "@/components/product_card";
import SectionHeader from "@/components/section_header";
import FilterMenu from "@/components/filter_menu";
import { useEffect, useState } from "react";
import { useCategporyState, useProductState } from "@/state/state";
import productAPIs from "@/api/product";
import { useTranslations } from "next-intl";
import ListProductCardSkeleton from "@/components/list_product_card_skeleton";

interface FilterOptions {
  categories: string[];
  priceRange: [number, number];
  minRating: number;
}

const ProductPage = () => {
  const router = useRouter();
  const pathname = usePathname();
  const t = useTranslations();
  const searchParams = useSearchParams();
  const [loading, setLoading] = useState(false);
  const [isHydrated, setIsHydrated] = useState(false);
  const [filteredProducts, setFilteredProducts] = useState<IProductData[]>([]);

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

  useEffect(() => {
    setFilteredProducts(productlist);
  }, [productlist]);

  const handleFilterChange = (filters: FilterOptions) => {
    let filtered = [...productlist];

    // Apply category filter
    if (filters.categories.length > 0) {
      filtered = filtered.filter((product) =>
        product.product_category.some((category) =>
          filters.categories.includes(category)
        )
      );
    }

    // Apply price filter
    filtered = filtered.filter(
      (product) =>
        product.price >= filters.priceRange[0] &&
        product.price <= filters.priceRange[1]
    );

    // Apply rating filter
    if (filters.minRating > 0) {
      filtered = filtered.filter(
        (product) => (product.product_avg_stars || 0) >= filters.minRating
      );
    }

    setFilteredProducts(filtered);
  };

  return (
    <div className="px-72 my-8 w-full">
      <div className="flex gap-8">
        <FilterMenu onFilterChange={handleFilterChange} categories={cateList} />
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
                {filteredProducts?.map((item: IProductData, index: number) => (
                  <ProductCard
                    key={index}
                    product={item}
                    onClick={() =>
                      router.push("/" + locale + "/product/" + item.product_id)
                    }
                  />
                ))}
              </div>
            )
          }
        />
      </div>
    </div>
  );
};

export default ProductPage;
