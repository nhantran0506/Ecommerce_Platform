import { API_BASE_URL, API_ROUTES } from "@/libraries/api";

class Cart {
  async addToCart(reqBody: IReqAddToCart): Promise<boolean> {
    const token = localStorage.getItem("token");

    const response = await fetch(
      `${API_BASE_URL}${API_ROUTES.ADD_PRODUCT_TO_CART}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(reqBody),
      }
    );

    if (!response.ok) {
      throw new Error(
        `Add product to cart failed with status ${response.status}`
      );
    }

    // const data = (await response.json()) as any;
    return true;
  }

  async getProductInCart(): Promise<IResCartProductList> {
    const token = localStorage.getItem("token");

    const response = await fetch(
      `${API_BASE_URL}${API_ROUTES.GET_PRODUCT_IN_CART}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error(
        `Add product to cart failed with status ${response.status}`
      );
    }

    const data = (await response.json()) as IResCartProductList;
    return data;
  }
}

export const cartAPIs = new Cart();
export default cartAPIs;
