import { IOrderItem } from "@/components/order_card";
import { OrderStatus } from "@/constant/enum";

export interface IOrder {
  id: string;
  status: OrderStatus;
  listOrderItem: IOrderItem[];
}

export interface IOrderHistory {
  order_id: string;
  created_at: string;
  product: {
    product_id: string;
    product_name: string;
    price: number;
    quantity: number;
  }[];
}
