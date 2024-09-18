"use client";
import FilterMenu from "@/components/filter_menu";
import {
  IFilterMenu,
  IOptionMenuFilter,
} from "@/components/filter_menu/interface";
import ProductCard from "@/components/product_card";
import SearchBar from "@/components/search";
import SectionHeader from "@/components/section_header";
import { Button } from "@nextui-org/react";
import { DollarSign, Filter, MapPin } from "react-feather";
import { productlist, recommendProductlist } from "./data";

const ProductPage = () => {
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
    <div className="flex justify-center my-8">
      <div className="flex flex-col">
        <div className="mb-8 flex">
          <div className="w-1/2 flex justify-start gap-4 pr-4">
            {listFilterMenu.map((item, index) => (
              <FilterMenu
                key={index}
                prefix={item.prefix}
                listFilterOption={item.listFilterOption}
              />
            ))}
          </div>
          <div className="w-1/2 flex justify-between">
            <SearchBar />

            <Button
              isIconOnly
              aria-label="Filter"
              radius="sm"
              className="w-10 h-10 bg-black"
            >
              <Filter className="text-white" />
            </Button>
          </div>
        </div>

        <SectionHeader
          title={"Recommended"}
          content={
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {recommendProductlist.map((item) => (
                <ProductCard key={item.id} product={item} />
              ))}
            </div>
          }
        />

        <SectionHeader
          title={"All Products"}
          content={
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {productlist.map((item) => (
                <ProductCard key={item.id} product={item} />
              ))}
            </div>
          }
        />
      </div>
    </div>
  );
};

export default ProductPage;
