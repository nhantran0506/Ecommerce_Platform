import { useState } from "react";
import { Filter, X } from "react-feather";
import FilterSection from "./filter_section";
import { ICheckBoxItem, IFilterMenuItem } from "./interface";
import ListCheckBox from "./list_checkbox";
import { Button, Input } from "@nextui-org/react";

const FilterMenu = () => {
  const [isOpen, setIsOpen] = useState(false);

  const togglePopup = () => {
    setIsOpen(!isOpen);
  };

  const listCheckboxCategories: ICheckBoxItem[] = [
    { name: "Devices" },
    { name: "Cloths" },
    { name: "Food" },
    { name: "Others" },
  ];

  const listFilterMenuItem: IFilterMenuItem[] = [
    {
      title: "Categories",
      content: <ListCheckBox listCheckBox={listCheckboxCategories} />,
    },
    {
      title: "Price",
      content: (
        <div className="flex items-center gap-4">
          <Input
            type="number"
            placeholder="0.00"
            labelPlacement="outside"
            startContent={
              <div className="pointer-events-none flex items-center">
                <span className="text-default-400 text-small">$</span>
              </div>
            }
          />
          <p className="font-bold">-</p>
          <Input
            type="number"
            placeholder="0.00"
            labelPlacement="outside"
            startContent={
              <div className="pointer-events-none flex items-center">
                <span className="text-default-400 text-small">$</span>
              </div>
            }
          />
        </div>
      ),
    },
  ];

  return (
    <div className="relative">
      <Button
        isIconOnly
        aria-label="Filter"
        radius="sm"
        className="w-10 h-10 bg-black"
        onClick={togglePopup}
      >
        <Filter className="text-white" />
      </Button>

      {/* Filter pop-up */}
      {isOpen && (
        <div className="absolute right-0 top-12 w-64 bg-white shadow-lg rounded-md p-4 z-50">
          {listFilterMenuItem.map((item, index) => (
            <div key={index} className="mb-4">
              <FilterSection title={item.title} content={item.content} />
            </div>
          ))}
          <div className="flex justify-between gap-2">
            <Button
              className="mt-2 w-full text-white"
              color="primary"
              onClick={() => {}}
            >
              Apply
            </Button>
            <Button
              className="mt-2"
              color="default"
              isIconOnly
              onClick={togglePopup}
            >
              <X />
            </Button>
          </div>
        </div>
      )}
    </div>
  );
};

export default FilterMenu;
