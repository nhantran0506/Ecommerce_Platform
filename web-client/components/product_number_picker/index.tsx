import { Button, Input } from "@nextui-org/react";
import { useState } from "react";
import { Minus, Plus } from "react-feather";

const ProductNumberPicker = () => {
  const maxNumberOfProduct = 10;
  const [numberOfProduct, setNumberOfProduct] = useState<number>(1);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value, 10);
    if (!isNaN(value) && value >= 1 && value <= maxNumberOfProduct) {
      setNumberOfProduct(value);
    }
  };

  return (
    <div className="flex items-center border-1 px-2 py-1 rounded-full">
      <Button
        isIconOnly
        radius="lg"
        className="bg-transparent"
        onClick={() =>
          setNumberOfProduct((numberOfProduct) =>
            numberOfProduct > 1 ? numberOfProduct - 1 : 1
          )
        }
      >
        <Minus size={15} />
      </Button>

      <input
        min={1}
        max={maxNumberOfProduct}
        value={numberOfProduct.toString()}
        onChange={handleInputChange}
        className="w-12 text-center text-medium"
      />

      <Button
        isIconOnly
        radius="lg"
        className="bg-transparent"
        onClick={() =>
          setNumberOfProduct((numberOfProduct) =>
            numberOfProduct < maxNumberOfProduct
              ? numberOfProduct + 1
              : maxNumberOfProduct
          )
        }
      >
        <Plus size={15} />
      </Button>
    </div>
  );
};

export default ProductNumberPicker;
