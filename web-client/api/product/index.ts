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

  async getSearchListProduct(input: string): Promise<IProductData[]> {
    const response = await fetch(
      `${API_BASE_URL}${API_ROUTES.GET_SEARCH_PRODUCTS}?user_query=${input}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    if (!response.ok) {
      throw new Error(
        `Get search products failed with status ${response.status}`
      );
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

  async getAllProductsShop(): Promise<IProductData[]> {
    const token = localStorage.getItem("token");

    const response = await fetch(
      `${API_BASE_URL}${API_ROUTES.GET_ALL_PRODUCTS_SHOP}`,
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
        `Get shop products failed with status ${response.status}`
      );
    }

    const data = (await response.json()) as IProductData[];
    return data;
  }

  async getRecommendedProducts(): Promise<IProductData[]> {
    const token = localStorage.getItem("token");
    const method = token ? "POST" : "GET";
    const headers: HeadersInit = {
      "Content-Type": "application/json",
    };

    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    const response = await fetch(
      `${API_BASE_URL}${API_ROUTES.GET_RECOMMENDED_PRODUCTS}`,
      {
        method,
        headers,
      }
    );

    if (!response.ok) {
      throw new Error(
        `Get recommended products failed with status ${response.status}`
      );
    }

    const data = (await response.json()) as IProductData[];
    return data;
  }

  async productRating(data: IProductRating): Promise<void> {
    const token = localStorage.getItem("token");
    const response = await fetch(
      `${API_BASE_URL}${API_ROUTES.PRODUCT_RATING}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          product_id: data.product_id,
          rating: data.rating,
          comment: data.comment || "",
        }),
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      throw { response: { status: response.status, ...errorData } };
    }
  }

  async getProductComments(
    productId: string
  ): Promise<IProductRatingResponse[]> {
    const response = await fetch(
      `${API_BASE_URL}/products/${productId}/comments`
    );
    if (!response.ok) {
      throw new Error("Failed to fetch product comments");
    }
    const data = await response.json();
    return data.map((comment: any) => ({
      user_name: `${comment.user_first_name} ${comment.user_last_name}`,
      rating: comment.rating,
      comment: comment.comment,
      created_at: comment.created_at,
    }));
  }

  async getAllCategories(): Promise<ICategory[]> {
    const response = await fetch(
      `${API_BASE_URL}${API_ROUTES.GET_CATEGORIES}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    if (!response.ok) {
      throw new Error(`Get categories failed with status ${response.status}`);
    }

    const data = (await response.json()) as ICategory[];
    return data;
  }
}

export const productAPIs = new Product();
export default productAPIs;
