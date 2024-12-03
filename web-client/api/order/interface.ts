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
