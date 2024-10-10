import { IProductData } from "../Product/IProductData";

export interface ICartItem {
  product: IProductData;
}

export interface ICartColumProp {
  key: string;
  label: string;
}
