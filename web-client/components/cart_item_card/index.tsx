import { ICartItem } from "@/interface/Cart/ICartUI";
import DefaultImage from "../product_card/default_image";
import { ImageSizeEnum } from "@/interface/Product/IProductUI";
import { Image } from "@nextui-org/react";

const CartItemCard: React.FC<ICartItem> = ({ product }) => {
  return (
    <div className="flex gap-4">
      {!product.image ? (
        <div className="w-[120px] h-[120px]">
          <DefaultImage imgSize={ImageSizeEnum.sm} />
        </div>
      ) : (
        <Image
          shadow="sm"
          radius="lg"
          width="100%"
          alt={product.product_name}
          className="w-[120px] h-[120px] object-cover"
          src={product.image}
          style={{
            objectFit: "cover",
            objectPosition: "center",
          }}
        />
      )}

      <div className="flex flex-col p-4 w-2/3">
        <h3 className="font-bold">{product.product_name}</h3>
        <p>{product.product_description}</p>
      </div>
    </div>
  );
};

export default CartItemCard;
