interface IReqAddToCart {
  product_id: string;
  quantity: number;
}

// interface IProductTable {
//   product_name: string;
//   product_id: string;
//   quantity: number;
//   product_price: number;
//   image_urls: string[];
//   total_price?: number;
// }

interface IResCartProductList {
  cart_details: {
    products: IProductData[];
    created_at: string;
    total_price: number;
  };
}

interface ICartModify {
  product_id: string;
  quantity: number;
}

interface IUpdateCartRequest {
  cart_items: ICartModify[];
}
