"use client";
import { truncateText } from "@/libraries/helpers";
import {
  Card,
  CardBody,
  CardFooter,
  CardHeader,
  Image,
} from "@nextui-org/react";
import { ShoppingCart } from "react-feather";
import StarRating from "../start_rating";

interface IProductCard {
  title: string;
  img: string;
  price: number;
  key: number;
}

const ProductCard: React.FC<IProductCard> = ({ title, img, price, key }) => {
  return (
    <Card
      className="border-2 rounded-xl w-[250px] h-[300px]"
      key={key}
      isPressable
      onPress={() => console.log("item pressed")}
    >
      <CardHeader className="overflow-visible p-0">
        <Image
          shadow="sm"
          radius="lg"
          width="100%"
          alt={title}
          className="w-full object-cover h-auto"
          src={img}
        />
      </CardHeader>
      <CardBody className=" items-start p-2">
        <p className="text-md line-clamp-1">{truncateText(title)}</p>
      </CardBody>
      <CardFooter className="justify-between">
        <div>
          <p className="font-bold text-xl">$ {price}</p>
          <StarRating totalStars={5} />
        </div>

        <div className="w-10 h-10 bg-black rounded-full flex items-center justify-center">
          <ShoppingCart size={25} color="white" />
        </div>
      </CardFooter>
    </Card>
  );
};

export default ProductCard;
