interface IOrderProduct {
  product_id: string;
  quantity: number;
}

interface IOrderResponse {
  success: boolean;
  payment_url: string;
}

interface IOrderDetails {
  order_id: string;
  product: {
    product_id: string;
    product_name: string;
    quantity: number;
    total: number;
  }[];
  created_at: string;
}

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
  created_at: string;
}
