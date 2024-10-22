import { Checkbox } from "@nextui-org/react";
import { IListCheckBox } from "../../../interface/UI/IFilterMenuUI";

const ListCheckBox: React.FC<IListCheckBox> = ({ listCheckBox }) => {
  return (
    <div className="flex flex-col gap-4">
      {listCheckBox.map((item, index) => (
        <Checkbox key={index} color="primary">
          {item.name}
        </Checkbox>
      ))}
    </div>
  );
};

export default ListCheckBox;
