import React, { useState } from "react";
import { ChevronDown, ChevronUp } from "react-feather";
import { IFilterMenuItem } from "../../../interface/UI/IFilterMenuUI";

const FilterSection: React.FC<IFilterMenuItem> = ({ title: name, content }) => {
  const [showContent, setShowContent] = useState(true);

  return (
    <>
      {/* Header */}
      <div
        className="flex justify-between items-center"
        onClick={() => setShowContent(!showContent)}
      >
        <p className="font-bold">{name}</p>
        {showContent ? <ChevronUp /> : <ChevronDown />}
      </div>

      {/* body */}
      {showContent ? <div className="mt-2">{content}</div> : <></>}
    </>
  );
};

export default FilterSection;
