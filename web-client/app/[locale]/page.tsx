"use client";
import { useRouter } from "next/navigation";
import { Button, Skeleton } from "@nextui-org/react";
import bannerImg from "@/assets/banner-bg.jpg";
import bannerImg2 from "@/assets/banner-2.jpeg";
import bannerImg3 from "@/assets/banner-3.jpg";
import SectionHeader from "@/components/section_header";
import ProductCard from "@/components/product_card";
import { ReactNode, useEffect, useState } from "react";
import productAPIs from "@/api/product";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import ListProductCardSkeleton from "@/components/list_product_card_skeleton";
import { useTranslations } from "next-intl";
import { CategoriesEnum } from "@/constant/enum";
import Image from "next/image";
import pantImg from "@/assets/pants.png";
import shirtImg from "@/assets/shirt.png";
import shoeImg from "@/assets/shoe.png";
import accessoriesImg from "@/assets/accessories.png";
import electronicsImg from "@/assets/electronics.png";
import booksImg from "@/assets/book.png";
import sportsImg from "@/assets/sports.png";
import makeupImg from "@/assets/makeup.png";
import healthImg from "@/assets/health.png";
import homeImg from "@/assets/home.png";
import toyImg from "@/assets/toy.png";
import foodImg from "@/assets/food.png";
import {
  useCategporyState,
  useLocaleState,
  useProductState,
} from "@/state/state";

export default function Home() {
  const router = useRouter();
  const t = useTranslations();
  const [loading, setLoading] = useState(false);
  const [isHydrated, setIsHydrated] = useState(false);

  const [recommendProductlist, setRecommendProductList] = useState<
    IProductData[]
  >([]);
  const productlist = useProductState((state) => state.productList);
  const setProductList = useProductState((state) => state.setProductList);
  const cateList = useCategporyState((state) => state.categoryList);
  const setCateList = useCategporyState((state) => state.setCategoryList);
  const locale = useLocaleState((state) => state.locale);

  useEffect(() => {
    setIsHydrated(true);
  }, []);

  useEffect(() => {
    fetchHomeInfo();
  }, []);

  const fetchHomeInfo = async () => {
    try {
      setLoading(true);

      if (isHydrated && productlist.length === 0) {
        const products = await productAPIs.getAll();
        setProductList(products);
      }

      const recommendedProducts = await productAPIs.getRecommendedProducts();
      setRecommendProductList(recommendedProducts);

      if (isHydrated && cateList.length === 0) {
        const cateListRes = await productAPIs.getAllCategories();
        setCateList(cateListRes);
      }
    } catch (error) {
      console.error("Failed to fetch home data:", error);
    } finally {
      setLoading(false);
    }
  };

  const bannerSettings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 3000,
    appendDots: (dots: any) => (
      <div style={{ position: "absolute", bottom: "-30px" }}>
        <ul style={{ margin: "0px" }}> {dots} </ul>
      </div>
    ),
    dotsClass: "slick-dots custom-dots",
  };

  const banners = [
    {
      image: bannerImg.src,
      title: "Shop the Best Deals of the Season!",
      subtitle: "Discover exclusive offers on your favorite products.",
    },
    {
      image: bannerImg3.src,
      title: "Special Holiday Offers",
      subtitle: "Limited time deals you won't want to miss.",
    },
    {
      image: bannerImg2.src,
      title: "New Arrivals Just Landed",
      subtitle: "Be the first to shop our latest collection.",
    },
  ];

  const renderCateIcon = (name: string): ReactNode => {
    switch (name) {
      case CategoriesEnum.SHIRT: {
        return (
          <Image src={shirtImg} alt="shirt-image" width={60} height={60} />
        );
      }
      case CategoriesEnum.PANTS: {
        return <Image src={pantImg} alt="pant-image" width={60} height={60} />;
      }
      case CategoriesEnum.SHOES: {
        return <Image src={shoeImg} alt="shoe-image" width={60} height={60} />;
      }
      case CategoriesEnum.ACCESSORIES: {
        return (
          <Image
            src={accessoriesImg}
            alt="accessories-image"
            width={60}
            height={60}
          />
        );
      }
      case CategoriesEnum.ELECTRONICS: {
        return (
          <Image
            src={electronicsImg}
            alt="electronics-image"
            width={60}
            height={60}
          />
        );
      }
      case CategoriesEnum.BOOKS: {
        return <Image src={booksImg} alt="book-image" width={50} height={50} />;
      }
      case CategoriesEnum.SPORTS: {
        return (
          <Image src={sportsImg} alt="sports-image" width={55} height={55} />
        );
      }
      case CategoriesEnum.BEAUTY: {
        return (
          <Image src={makeupImg} alt="make-up-image" width={60} height={60} />
        );
      }
      case CategoriesEnum.HEALTH: {
        return (
          <Image src={healthImg} alt="health-image" width={60} height={60} />
        );
      }
      case CategoriesEnum.HOME: {
        return <Image src={homeImg} alt="home-image" width={50} height={50} />;
      }
      case CategoriesEnum.TOYS: {
        return <Image src={toyImg} alt="toy-image" width={50} height={50} />;
      }
      case CategoriesEnum.FOOD: {
        return <Image src={foodImg} alt="food-image" width={55} height={55} />;
      }
      default: {
        return <div className="text-3xl font-bold">...</div>;
      }
    }
  };

  return (
    <div className="flex flex-col mx-64">
      {/* Banner Section */}
      <div className="relative mx-auto my-8 w-full">
        <Slider {...bannerSettings}>
          {banners.map((banner, index) => (
            <div key={index}>
              <div className="relative">
                {/* Overlay content */}
                <div className="absolute top-0 left-0 right-0 bottom-0 flex justify-center items-center z-10 bg-black bg-opacity-30 rounded-xl">
                  <div className="text-center text-white">
                    <h1 className="text-4xl font-bold">{banner.title}</h1>
                    <p className="text-sm">{banner.subtitle}</p>
                  </div>
                </div>

                {/* Image */}
                <div className="relative w-full h-[400px]">
                  <Image
                    src={banner.image}
                    alt={`Banner Image ${index + 1}`}
                    layout="fill"
                    objectFit="cover"
                    className="rounded-xl"
                  />
                </div>
              </div>
            </div>
          ))}
        </Slider>
      </div>

      {/* Content Section */}
      {loading ? (
        <SectionHeader
          title={t("home_category")}
          content={
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
              {Array.from({ length: 8 }).map((_, index) => (
                <Skeleton
                  key={index}
                  className="w-24 h-24 rounded-lg"
                ></Skeleton>
              ))}
            </div>
          }
        />
      ) : cateList.length > 0 ? (
        <SectionHeader
          title={t("home_category")}
          content={
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-8 gap-4">
              {cateList.map((item: ICategory, index: number) => (
                <Button
                  isIconOnly
                  className="w-24 h-24 border-3 border-black bg-white shadow-lg"
                  key={index}
                >
                  {renderCateIcon(item.category_name)}
                </Button>
              ))}
            </div>
          }
        />
      ) : (
        <></>
      )}

      {loading ? (
        <SectionHeader
          title={t("products_recommend_product")}
          content={<ListProductCardSkeleton gridCols={4} count={4} />}
        />
      ) : recommendProductlist.length > 0 ? (
        <SectionHeader
          title={t("products_recommend_product")}
          content={
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {recommendProductlist.map((item: IProductData, index: number) => (
                <ProductCard
                  key={index}
                  product={item}
                  onClick={() =>
                    router.push("/" + locale + "/product/" + item.product_id)
                  }
                />
              ))}
            </div>
          }
        />
      ) : (
        <></>
      )}

      {loading ? (
        <SectionHeader
          title={t("products_all_product")}
          content={<ListProductCardSkeleton gridCols={4} count={4} />}
        />
      ) : productlist.length > 0 ? (
        <SectionHeader
          title={t("products_all_product")}
          content={
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {productlist.map((item: IProductData, index: number) => (
                <ProductCard
                  key={index}
                  product={item}
                  onClick={() =>
                    router.push("/" + locale + "/product/" + item.product_id)
                  }
                />
              ))}
            </div>
          }
        />
      ) : (
        <></>
      )}
    </div>
  );
}
