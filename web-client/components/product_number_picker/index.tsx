import { Button, Input } from "@nextui-org/react";
import { useState } from "react";
import { Minus, Plus } from "react-feather";

interface IProductNumberPicker {
  id: string;
  value: number;
  setValue: (id: string, val: number) => void;
  maxNumberOfProduct: number;
}

const ProductNumberPicker: React.FC<IProductNumberPicker> = ({
  id,
  value,
  setValue,
  maxNumberOfProduct,
}) => {
  const [numberOfProduct, setNumberOfProduct] = useState<number>(value);

  const handleInputType = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value, 10);
    if (!isNaN(value) && value >= 1 && value <= maxNumberOfProduct) {
      setNumberOfProduct(value);
      await setValue(id, value);
    }
  };

  // update api
  const handleIncreaseValue = async () => {
    await setNumberOfProduct((prevNumberOfProduct) => {
      const updatedValue =
        prevNumberOfProduct > 1 ? prevNumberOfProduct - 1 : 1;
      setValue(id, updatedValue);
      return updatedValue;
    });
  };

  const handleDecreaseValue = async () => {
    await setNumberOfProduct((prevNumberOfProduct) => {
      const updatedValue =
        prevNumberOfProduct < maxNumberOfProduct
          ? prevNumberOfProduct + 1
          : maxNumberOfProduct;
      setValue(id, updatedValue);
      return updatedValue;
    });
  };

  return (
    <div className="flex items-center border-1 px-2 py-1 rounded-full w-36">
      <Button
        isIconOnly
        radius="full"
        variant="light"
        onClick={() => handleIncreaseValue()}
      >
        <Minus size={15} />
      </Button>

      <input
        min={1}
        max={maxNumberOfProduct}
        value={numberOfProduct.toString()}
        onChange={handleInputType}
        className="w-12 text-center text-medium"
      />

      <Button
        isIconOnly
        radius="full"
        variant="light"
        onClick={() => handleDecreaseValue()}
      >
        <Plus size={15} />
      </Button>
    </div>
  );
};

export default ProductNumberPicker;
