interface IReqAddToCart {
  product_id: string;
  quantity: number;
}

interface IProductInCart {
  product_name: string;
  product_id: string;
  quantity: number;
  price: number;
  total_price: number;
}

interface IResCartProductList {
  cart_details: {
    products: IProductInCart[];
    created_at: string;
  };
}
