import { API_BASE_URL, API_ROUTES } from "@/libraries/api";

class Product {
  async getAll(): Promise<IProductData[]> {
    const response = await fetch(
      `${API_BASE_URL}${API_ROUTES.GET_ALL_PRODUCT}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    if (!response.ok) {
      throw new Error(`Get products failed with status ${response.status}`);
    }

    const data = (await response.json()) as IProductData[];
    return data;
  }

  async getProductById(id: string): Promise<IProductDetailData> {
    const token = localStorage.getItem("token");

    const response = await fetch(
      `${API_BASE_URL}${API_ROUTES.GET_PRODUCT_DETAIL}/${id}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response.ok) {
      throw new Error(`Get products failed with status ${response.status}`);
    }

    const data = (await response.json()) as IProductDetailData;
    return data;
  }
}

export const productAPIs = new Product();
export default productAPIs;
