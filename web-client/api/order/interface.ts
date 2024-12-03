interface IOrderProduct {
  product_id: string;
  quantity: number;
}

interface IOrderResponse {
  success: boolean;
  payment_url: string;
}

<<<<<<< Updated upstream
interface IOrderDetails {
  order_id: string;
  product: {
    product_id: string;
    product_name: string;
    quantity: number;
    total: number;
  }[];
=======
interface IOrderHistoryProduct {
  product_id: string;
  product_name: string;
  product_description: string;
  price: number;
  quantity: number;
  total: number;
}

interface IOrderHistory {
  order_id: string;
  product: IOrderHistoryProduct[];
>>>>>>> Stashed changes
  created_at: string;
}
