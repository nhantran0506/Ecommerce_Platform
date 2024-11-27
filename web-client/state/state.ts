import { create } from "zustand";
import { UserRoleEnum } from "./enum";

// // Define the store types
// interface CounterState {
//   count: number;
//   increase: () => void;
//   decrease: () => void;
//   reset: () => void;
// }

// // // Create the store
// export const useCounterStore = create<CounterState>((set) => ({
//   count: 0, // Initial state

//   // Action to increase the count
//   increase: () => set((state) => ({ count: state.count + 1 })),

//   // Action to decrease the count
//   decrease: () => set((state) => ({ count: state.count - 1 })),

//   // Action to reset the count
//   reset: () => set({ count: 0 }),
// }));

export const useProductId = create<IProductId>((set) => ({
  productId: "",
  setProductId: (newId) => set(() => ({ productId: newId })),
}));

export const userState = create<IUserState>((set) => ({
  user: {
    first_name: "",
    last_name: "",
    phone_number: "",
    address: "",
    email: "",
    role: UserRoleEnum.user,
  },

  setUser: (userInfo: IUserData) => set(() => ({ user: userInfo })),
  clearUser: () =>
    set({
      user: {
        first_name: "",
        last_name: "",
        phone_number: "",
        address: "",
        email: "",
        role: UserRoleEnum.user,
      },
    }),
}));

export const productState = create<IListProductState>((set) => ({
  productList: [],

  setProductList: (productList: IProductData[]) =>
    set(() => ({ productList: productList })),

  clearProductList: () => set({ productList: [] }),
}));
