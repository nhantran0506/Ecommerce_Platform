import React from "react";
import { Select, SelectItem } from "@nextui-org/react";
import { IFilterMenu } from "./interface";

const SingleComboBoxItem: React.FC<IFilterMenu> = ({
  prefix,
  listFilterOption,
}) => {
  return (
    <div className="flex gap-1 items-center w-full">
      <div className="flex items-center mr-1.5">{prefix}</div>

      <div className="w-full flex flex-col gap-4">
        <div className="flex flex-col gap-2">
          <div className="flex w-full flex-wrap items-end md:flex-nowrap mb-6 md:mb-0 gap-4">
            <Select
              labelPlacement={"outside-left"}
              className="w-full"
              aria-label="Filter combobox"
            >
              {listFilterOption.map((item) => (
                <SelectItem key={item.key}>{item.label}</SelectItem>
              ))}
            </Select>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SingleComboBoxItem;
