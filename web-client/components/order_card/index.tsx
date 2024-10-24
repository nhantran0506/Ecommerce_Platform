"use client";
import { OrderStatus } from "@/constant/enum";
import { IProductData } from "@/interface/Data/IProductData";
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Divider,
  Button,
} from "@nextui-org/react";
import { Calendar, Clock } from "lucide-react";
import { useRouter } from "next/navigation";
import { ReactNode } from "react";

interface IOrderCardInfo {
  name: string;
  icon: ReactNode;
  value: string;
}

export interface IOrderItem {
  product: IProductData;
  number: number;
}

interface IOrderCard {
  id: string;
  status: OrderStatus;
  listOrderItem: IOrderItem[];
}

const OrderCard: React.FC<IOrderCard> = ({ id, status, listOrderItem }) => {
  const router = useRouter();

  const listOrderCardOption: IOrderCardInfo[] = [
    {
      name: "date",
      icon: <Calendar />,
      value: "September 16, 2020",
    },
    {
      name: "time",
      icon: <Clock />,
      value: "11:54 PM",
    },
  ];

  const navigateToOrderDetail = () => {
    router.push(`/order/${id}`);
  };

  return (
    <Card className="max-w-[400px] bg-[#F7F7F7]">
      <CardHeader className="flex justify-between">
        <div>
          <p className="text-xl font-bold">Order #{id}</p>
        </div>

        <Card
          className="bg-green-400 text-white font-semibold px-2 py-1"
          radius="lg"
        >
          {status}
        </Card>
      </CardHeader>
      <Divider />
      <CardBody>
        <div className="flex gap-4 mb-4">
          {listOrderCardOption.map((item, index) => (
            <div key={index} className="flex gap-2">
              {item.icon}
              <p>{item.value}</p>
            </div>
          ))}
        </div>

        <div className="flex flex-col">
          {listOrderItem.map((item, index) => (
            <div className="flex gap-2 mb-2 items-center" key={index}>
              <div className="w-7 h-7 flex items-center justify-center rounded-md bg-white">
                {item.number}
              </div>
              <p className="font-bold">{item.product.product_name}</p>
            </div>
          ))}
        </div>
      </CardBody>
      <Divider />
      <CardFooter className="flex justify-between gap-4">
        <Button
          className="w-full rounded-full bg-black text-white font-bold"
          onPress={() => navigateToOrderDetail()}
        >
          Details
        </Button>
        <Button
          className="w-full rounded-full font-bold"
          color="danger"
          variant="bordered"
        >
          Cancel
        </Button>
      </CardFooter>
    </Card>
  );
};

export default OrderCard;
