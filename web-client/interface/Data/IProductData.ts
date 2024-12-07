interface IShopProductData {
  id: string;
  product_name: string;
  product_description: string;
  price: number;
  create_at_datetime?: string;
  lastUpdate: string;
  image?: string;
  product_category: string[];
}

interface IProductData {
  id: string;
  product_name: string;
  product_description: string;
  price: number;
  create_at_datetime?: string;
  lastUpdate: string;
  image?: string;
  product_category: string[];
}
