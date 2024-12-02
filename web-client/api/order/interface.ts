interface IOrderProduct {
  product_id: string;
  quantity: number;
}

interface IOrderResponse {
  success: boolean;
  payment_url: string;
}
