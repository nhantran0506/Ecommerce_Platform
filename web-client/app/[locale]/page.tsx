"use client";
import { useRouter } from "next/navigation";
import { Image } from "@nextui-org/react";
import bannerImg from "@/assets/banner-bg.jpg";
import SectionHeader from "@/components/section_header";
import ProductCard from "@/components/product_card";

export default function Home() {
  return (
    <div className="flex flex-col mx-64">
      {/* Banner Section */}
      <div className="relative mx-auto my-8 w-full">
        {/* Overlay content */}
        <div className="absolute top-0 left-0 right-0 bottom-0 flex justify-center items-center z-10 bg-black bg-opacity-25 rounded-xl">
          <div className="text-center text-white">
            <h1 className="text-4xl font-bold">
              {"Shop the Best Deals of the Season!"}
            </h1>
            <p className="text-sm">
              {"Discover exclusive offers on your favorite products."}
            </p>
          </div>
        </div>

        {/* Image */}
        <Image
          src={bannerImg.src}
          alt="Banner Image"
          className="object-cover object-[50%_60%] h-[400px] z-0 rounded-xl"
          width={1100}
        />
      </div>

      {/* Content Section */}
      {/* <SectionHeader
        title={"All Products"}
        content={
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {productlist.map((item, index) => (
              <ProductCard
                key={index}
                product={item}
                onClick={() => router.push("/product/" + item.id)}
              />
            ))}
          </div>
        }
      /> */}
    </div>
  );
}
