"use client";
import { truncateText } from "@/libraries/helpers";
import { Card, CardBody, CardFooter, Image } from "@nextui-org/react";
import { ShoppingCart } from "react-feather";
import StarRating from "../start_rating";
import DefaultImage from "./default_image";
import { ImageSizeEnum } from "@/interface/UI/IProductUI";

interface IProductCard {
  product: IProductData;
  onClick: () => void;
}

const DEFAULT_IMAGE_URL = "https://via.placeholder.com/220x180?text=No+Image";

const ProductCard: React.FC<IProductCard> = ({ product, onClick }) => {
  const imageUrl = product.image_urls?.[0] || DEFAULT_IMAGE_URL;
  const isOutOfStock = product.inventory === 0;

  return (
    <Card
      className="border-2 rounded-xl w-[220px] h-[300px]"
      isPressable
      onPress={() => onClick()}
    >
      <CardBody className="overflow-visible p-0 relative">
        <Image
          shadow="sm"
          radius="lg"
          width="100%"
          alt={product.product_name}
          className={`w-full h-[180px] object-cover ${isOutOfStock ? 'opacity-50' : ''}`}
          src={imageUrl}
          style={{
            objectFit: "cover",
            objectPosition: "center",
          }}
        />
        {isOutOfStock && (
          <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-30 rounded-lg">
            <span className="text-white font-bold text-lg">Out of Stock</span>
          </div>
        )}
      </CardBody>
      <CardFooter>
        <div className="flex flex-col w-full h-full">
          <p className="text-lg line-clamp-1 text-start">
            {product.product_name}
          </p>

          <div className="flex justify-between items-center">
            <div className="flex flex-col items-start">
              <p className="font-bold text-lg">$ {product.product_price}</p>
              <StarRating
                totalStars={5}
                initStart={product.product_avg_stars}
                readonly
              />
              <p className="text-sm">
                Sold{" "}
                <span className="font-semibold text-primary-300">
                  {product.product_total_sales}
                </span>{" "}
                items
              </p>
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
