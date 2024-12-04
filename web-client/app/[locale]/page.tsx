"use client";
import { useRouter } from "next/navigation";
import { Image } from "@nextui-org/react";
import bannerImg from "@/assets/banner-bg.jpg";
import bannerImg2 from "@/assets/banner-2.jpeg";
import bannerImg3 from "@/assets/banner-3.jpg";
import SectionHeader from "@/components/section_header";
import ProductCard from "@/components/product_card";
import { useEffect, useState } from "react";
import productAPIs from "@/api/product";
import { usePathname } from "next/navigation";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import ListProductCardSkeleton from "@/components/list_product_card_skeleton";
import { useTranslations } from "next-intl";

export default function Home() {
  const router = useRouter();
  const pathname = usePathname();
  const locale = pathname.split("/")[1];
  const [loading, setLoading] = useState(false);
  const [productlist, setProductList] = useState<IProductData[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const t = useTranslations();

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
                <Image
                  src={banner.image}
                  alt={`Banner Image ${index + 1}`}
                  className="object-cover object-[50%_60%] h-[400px] z-0 rounded-xl"
                  width={1100}
                />
              </div>
            </div>
          ))}
        </Slider>
      </div>

      {/* Content Section */}
      <SectionHeader
        title={t("products_all_product")}
        content={
          loading ? (
            <ListProductCardSkeleton gridCols={4} count={4} />
          ) : (
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
          )
        }
      />
    </div>
  );
}
