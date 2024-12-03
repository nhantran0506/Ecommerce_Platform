"use client";

import { useEffect, useState, useCallback } from "react";
import { API_BASE_URL, API_ROUTES } from "@/libraries/api";
import SectionHeader from "@/components/section_header";
import IframeContainer from "@/components/iframe_container";
import Spinner from "@/components/spinner";

export default function ShopDashboard() {
  const [iframeSrcs, setIframeSrcs] = useState<{
    revenueStats: string;
    topProductsStats: string;
    categoryStats: string;
  }>({
    revenueStats: "",
    topProductsStats: "",
    categoryStats: "",
  });

  const [isLoading, setIsLoading] = useState(true);

  const fetchChart = useCallback(async (endpoint: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({ "timestamp": Date.now() }),
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch chart from ${endpoint}`);
      }

      const chartHtml = await response.text();
      const blob = new Blob([chartHtml], { type: "text/html" });
      return URL.createObjectURL(blob);
    } catch (error) {
      console.error(`Error fetching chart from ${endpoint}:`, error);
      return "";
    }
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);

      const revenueStatsSrc = await fetchChart(API_ROUTES.SHOP_REVENUE_STATS);
      const topProductsStatsSrc = await fetchChart(API_ROUTES.SHOP_TOP_PRODUCTS_STATS);
      const categoryStatsSrc = await fetchChart(API_ROUTES.SHOP_CATEGORIES_STATS);

      setIframeSrcs({
        revenueStats: revenueStatsSrc,
        topProductsStats: topProductsStatsSrc,
        categoryStats: categoryStatsSrc,
      });

      setIsLoading(false);
    };

    fetchData();

    return () => {
      Object.values(iframeSrcs).forEach((src) => {
        if (src) URL.revokeObjectURL(src);
      });
    };
  }, [fetchChart]);

  if (isLoading) {
    return <Spinner />;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-8">Shop Dashboard</h1>

      <div className="space-y-8">
        <div className="grid grid-cols-1 gap-6">
          <IframeContainer 
            title="Revenue Overview" 
            src={iframeSrcs.revenueStats} 
          />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <IframeContainer 
            title="Top Products" 
            src={iframeSrcs.topProductsStats} 
          />
          <IframeContainer 
            title="Categories Overview" 
            src={iframeSrcs.categoryStats} 
          />
        </div>
      </div>
    </div>
  );
}
