interface IUserData {
  first_name: string;
  last_name: string;
  phone_number: string;
  address: string;
  email: string;
  role: UserRoleEnum;
}

interface IUserState {
  user: IUserData;
  setUser: (userInfo: IUserData) => void;
  clearUser: () => void;
}

interface IProductId {
  productId: string;
  setProductId: (newId: string) => void;
}

interface IListProductState {
  productList: IProductData[];

  setProductList: (productList: IProductData[]) => void;
  clearProductList: () => void;
}
