import { IResGetUser } from "@/api/auth/interface";
import { LocaleEnum } from "./enum";

export interface IUserState {
  user: IResGetUser;
  setUser: (userInfo: IResGetUser) => void;
  clearUser: () => void;
}

export interface IProductId {
  productId: string;
  setProductId: (newId: string) => void;
}

export interface IListProductState {
  productList: IProductData[];

  setProductList: (productList: IProductData[]) => void;
  clearProductList: () => void;
}

export interface IListCategoryState {
  categoryList: ICategory[];

  setCategoryList: (categoryList: ICategory[]) => void;
  clearCategoryList: () => void;
}

export interface ILocaleState {
  locale: LocaleEnum;

  setLocale: (locale: LocaleEnum) => void;
  clearLocale: () => void;
}
