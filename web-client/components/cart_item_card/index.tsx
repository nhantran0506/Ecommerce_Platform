import { ICartItem } from "@/interface/UI/ICartUI";
import DefaultImage from "../product_card/default_image";
import { ImageSizeEnum } from "@/interface/UI/IProductUI";
import { Button, Card, Image } from "@nextui-org/react";

const CartItemCard: React.FC<ICartItem> = ({ product, onClick }) => {
  return (
    <Card
      className="p-2 shadow-none"
      isPressable
      onPress={() => onClick()}
      isHoverable
    >
      <div className="flex gap-4">
        <Button isIconOnly className="w-[120px] h-[120px]">
          {product?.image ? (
            <div className="w-[120px] h-[120px]">
              <DefaultImage imgSize={ImageSizeEnum.sm} />
            </div>
          ) : (
            <Image
              shadow="sm"
              radius="lg"
              width="100%"
              alt={product?.product_name}
              className="w-[120px] h-[120px] object-cover"
              src={product?.image}
              style={{
                objectFit: "cover",
                objectPosition: "center",
              }}
            />
          )}
        </Button>

        <div className="flex flex-col p-2 w-2/3 text-start">
          <h3 className="font-bold mb-1 text-lg line-clamp-1">
            {product?.product_name}
          </h3>
          <p className="line-clamp-3">{product?.product_description}</p>
        </div>
      </div>
    </Card>
  );
};

export default CartItemCard;
