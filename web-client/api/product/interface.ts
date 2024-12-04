interface IProductData {
  product_id: string;
  product_name: string;
  price: number;
  image_urls: string[];
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
