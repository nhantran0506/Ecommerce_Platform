interface IProductData {
  product_id: string;
  product_name: string;
  product_price: number;
  image_urls: string[];
}

interface IProductDetailData {
  product_id: string;
  product_name: string;
  product_description: string;
  product_category: string[];
  price: number;
  image_urls: string[];
}
