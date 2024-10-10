"use client";
import { truncateText } from "@/libraries/helpers";
import { Card, CardBody, CardFooter, Image } from "@nextui-org/react";
import { ShoppingCart } from "react-feather";
import StarRating from "../start_rating";
import DefaultImage from "./default_image";
import { ImageSizeEnum } from "@/interface/Product/IProductUI";
import { IProductData } from "@/interface/Product/IProductData";

interface IProductCard {
  product: IProductData;
  onClick: () => void;
}

const ProductCard: React.FC<IProductCard> = ({ product, onClick }) => {
  return (
    <Card
      className="border-2 rounded-xl w-[220px] h-[280px]"
      isPressable
      onPress={() => onClick()}
    >
      <CardBody className="overflow-visible p-0">
        {!product.image ? (
          <div className="h-full w-full">
            <DefaultImage imgSize={ImageSizeEnum.md} />
          </div>
        ) : (
          <Image
            shadow="sm"
            radius="lg"
            width="100%"
            alt={product.product_name}
            className="w-full h-[180px] object-cover"
            src={product.image}
            style={{
              objectFit: "cover",
              objectPosition: "center",
            }}
          />
        )}
      </CardBody>
      <CardFooter>
        <div className="flex flex-col w-full h-full">
          <p className="text-md line-clamp-1 text-start">
            {truncateText(product.product_name)}
          </p>

          <div className="flex justify-between">
            <div className="flex flex-col items-start">
              <p className="font-bold text-lg">$ {product.price}</p>
              <StarRating totalStars={5} />
            </div>

            <div className="w-10 h-10 bg-black rounded-full flex items-center justify-center">
              <ShoppingCart size={25} color="white" />
            </div>
          </div>
        </div>
      </CardFooter>
    </Card>
  );
};

export default ProductCard;
