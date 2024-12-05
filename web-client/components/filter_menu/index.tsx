import { useState } from "react";
import { Filter, X } from "react-feather";
import FilterSection from "./filter_section";
import {
  ICheckBoxItem,
  IFilterMenuItem,
} from "../../interface/UI/IFilterMenuUI";
import ListCheckBox from "./list_checkbox";
import { Button, Input, Checkbox } from "@nextui-org/react";

const FilterMenu = () => {
  const categories = [
    {
      title: "Categories",
      items: [
        { name: "Devices (12k+)", checked: false },
        { name: "Cloths (12k+)", checked: false },
        { name: "Food (11k+)", checked: false },
        { name: "Others (10k+)", checked: false },
      ],
    },
    {
      title: "Location",
      items: [
        { name: "Ha Noi", checked: false },
        { name: "Ho Chi Minh", checked: false },
        { name: "Thai Nguyen", checked: false },
        { name: "Vinh Phuc", checked: false },
      ],
    },
  ];

  return (
    <div className="w-48 border rounded-lg p-4 h-[380px]">
      <h2 className="text-lg font-bold mb-4">FILTER</h2>

      {categories.map((category, index) => (
        <div key={index} className="mb-6">
          <h3 className="font-medium mb-2">{category.title}</h3>
          <div className="flex flex-col gap-2">
            {category.items.map((item, itemIndex) => (
              <div key={itemIndex} className="flex items-center gap-2">
                <Checkbox size="sm">{item.name}</Checkbox>
              </div>
            ))}
          </div>
          {/* <button className="text-sm text-gray-600 mt-2">More</button> */}
        </div>
      ))}
    </div>
  );
};

export default FilterMenu;
