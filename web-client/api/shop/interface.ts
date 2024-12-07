interface IReqCreateShop {
  shop_name: string;
  shop_address: string;
  shop_bio: string;
}

interface IResCurrentShopDetail {
  shop_name: string;
  shop_address: string;
  shop_bio: string;
  avg_stars: number;
  shop_id: string;
  shop_phone_number: string;
  owner_id: string;
  total_ratings: number;
}
