import { IOrderItem } from "@/components/order_card";
import { OrderStatus } from "@/constant/enum";

export interface IOrder {
  id: string;
  status: OrderStatus;
  listOrderItem: IOrderItem[];
}
