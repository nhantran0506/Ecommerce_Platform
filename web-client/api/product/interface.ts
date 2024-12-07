interface IProductData {
  product_id: string;
  product_name: string;
  price: number;
  image_urls: string[];
  product_total_ratings: number;
  product_avg_stars: number;
  product_total_sales: number;
  inventory: number;
}

interface IProductDetailData {
  product_id: string;
  product_name: string;
  product_description: string;
  product_category: string[];
  product_avg_stars: number;
  product_total_ratings: number;
  product_total_sales: number;
  price: number;
  inventory: number;
  image_urls: string[];
  shop_name: {
    shop_id: string;
    shop_name: string;
  };
}

interface IProductRating {
  product_id: string;
  rating: number;
  comment?: string;
}

interface IProductRatingResponse {
  user_name: string;
  rating: number;
  comment: string;
  created_at: string;
}

interface ICategory {
  category_id: string;
  category_name: string;
}
