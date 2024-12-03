import DefaultImage from "../product_card/default_image";
import { ImageSizeEnum } from "@/interface/UI/IProductUI";
import { Card, Image } from "@nextui-org/react";

const CartItemCard: React.FC<ICartItem> = ({ product, onClick }) => {
  return (
    <Card
      className="p-2 shadow-none"
      isPressable
      onPress={() => onClick()}
      isHoverable
    >
      <div className="flex gap-4">
        <div className="w-[200px] h-[120px] flex items-center justify-center">
          {product?.image_urls[0] == "" ? (
            <div className="w-[120px] h-[120px]">
              <DefaultImage imgSize={ImageSizeEnum.sm} />
            </div>
          ) : (
            <Image
              shadow="sm"
              radius="lg"
              width="100%"
              alt={product.product_name}
              className="w-full h-[180px] object-cover"
              src={product.image_urls[0]}
              style={{
                objectFit: "cover",
                objectPosition: "center",
              }}
            />
          )}
        </div>

        <div className="flex flex-col p-2 w-2/3 text-start">
          <h3 className="font-bold mb-1 text-lg line-clamp-1">
            {product?.product_name}
          </h3>
        </div>
      </div>
    </Card>
  );
};

export default CartItemCard;
