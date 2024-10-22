import { create } from "zustand";

// // Define the store types
// interface CounterState {
//   count: number;
//   increase: () => void;
//   decrease: () => void;
//   reset: () => void;
// }

// // Create the store
// export const useCounterStore = create<CounterState>((set) => ({
//   count: 0, // Initial state

//   // Action to increase the count
//   increase: () => set((state) => ({ count: state.count + 1 })),

//   // Action to decrease the count
//   decrease: () => set((state) => ({ count: state.count - 1 })),

//   // Action to reset the count
//   reset: () => set({ count: 0 }),
// }));

interface IProductId {
  productId: string;
  setProductId: (newId: string) => void;
}

export const useProductId = create<IProductId>((set) => ({
  productId: "",
  setProductId: (newId) => set(() => ({ productId: newId })),
}));
