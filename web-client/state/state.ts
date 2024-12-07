import { create } from "zustand";
import { persist } from "zustand/middleware";
import {
  IListCategoryState,
  IListProductState,
  ILocaleState,
  IProductId,
  IUserState,
} from "./interface";
import { LocaleEnum } from "./enum";
import { IResGetUser } from "@/api/auth/interface";

export const useProductId = create<IProductId>((set) => ({
  productId: "",
  setProductId: (newId) => set(() => ({ productId: newId })),
}));

export const useUserState = create<IUserState>((set) => ({
  user: {
    user_id: "",
    first_name: "",
    last_name: "",
    phone_number: "",
    address: "",
    email: "",
    role: "",
    dob: "",
  },

  setUser: (userInfo: IResGetUser) => set(() => ({ user: userInfo })),
  clearUser: () =>
    set({
      user: {
        user_id: "",
        first_name: "",
        last_name: "",
        phone_number: "",
        address: "",
        email: "",
        role: "",
        dob: "",
      },
    }),
}));

export const useProductState = create(
  persist<IListProductState>(
    (set) => ({
      productList: [],
      setProductList: (productList: IProductData[]) =>
        set(() => ({ productList: productList })),
      clearProductList: () => set({ productList: [] }),
    }),
    {
      name: "product-storage",
    }
  )
);

export const useCategporyState = create(
  persist<IListCategoryState>(
    (set) => ({
      categoryList: [],
      setCategoryList: (categoryList: ICategory[]) =>
        set(() => ({ categoryList: categoryList })),
      clearCategoryList: () => set({ categoryList: [] }),
    }),
    {
      name: "category-storage",
    }
  )
);

export const useLocaleState = create(
  persist<ILocaleState>(
    (set) => ({
      locale: LocaleEnum.en,
      setLocale: (locale: LocaleEnum) => set(() => ({ locale: locale })),
      clearLocale: () => set({ locale: LocaleEnum.en }),
    }),
    {
      name: "locale-storage",
    }
  )
);
