import { IProductData } from "../Data/IProductData";

export interface ICartItem {
  product: IProductData;
  onClick: () => void;
}

export interface ITableColumProp {
  key: string;
  label: string;
}
