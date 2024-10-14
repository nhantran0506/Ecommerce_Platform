"use client";

import { useEffect, useState, useCallback } from "react";
import { API_BASE_URL, API_ROUTES } from "@/libraries/api";
import StatCard from "@/components/stat_card";
import IframeContainer from "@/components/iframe_container";

export default function AdminPage() {
  const [stats, setStats] = useState({
    usersOnline: "0",
    revenue: "$0",
    shopCount: "0",
  });

  const [iframeSrcs, setIframeSrcs] = useState<{
    userActivity: string ;
    salesOverview: string ;
    productPerformance: string ;
  }>({
    userActivity: "",
    salesOverview: "",
    productPerformance: "",
  });

  const fetchNumber = useCallback(
    async (endpoint: string, field: keyof typeof stats) => {
      try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
          method: "POST", 
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });

        if (!response.ok) {
          throw new Error(`Failed to fetch ${field} from ${endpoint}`);
        }

        const data = await response.json();

        const value = data[field];

        if (field === "revenue") {
          setStats((prevStats) => ({
            ...prevStats,
            [field]: `$${Number(value).toLocaleString()}`,
          }));
        } else {
          setStats((prevStats) => ({
            ...prevStats,
            [field]: String(value),
          }));
        }
      } catch (error) {
        console.error(`Error fetching ${field} from ${endpoint}:`, error);
        setStats((prevStats) => ({
          ...prevStats,
          [field]: "N/A",
        }));
      }
    },
    []
  );

  const fetchChart = useCallback(async (endpoint: string) => {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
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
    fetchNumber(API_ROUTES.USERS_NUMBER, "usersOnline");
    fetchNumber(API_ROUTES.REVENUE_CURRENT, "revenue");
    fetchNumber(API_ROUTES.SHOPS_NUMBER, "shopCount");

    const fetchAllCharts = async () => {
      const userActivitySrc = await fetchChart(API_ROUTES.USERS_NUMBER);
      const salesOverviewSrc = await fetchChart(API_ROUTES.REVENUE_CURRENT);
      const productPerformanceSrc = await fetchChart(API_ROUTES.SHOPS_NUMBER);

      setIframeSrcs({
        userActivity: userActivitySrc,
        salesOverview: salesOverviewSrc,
        productPerformance: productPerformanceSrc,
      });
    };

    fetchAllCharts();

    return () => {
      Object.values(iframeSrcs).forEach((src) => {
        if (src) URL.revokeObjectURL(src);
      });
    };
  }, [fetchChart, fetchNumber, iframeSrcs]);

  return (
    <div className="p-8 max-w-7xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">Admin Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <StatCard title="Users Online" value={stats.usersOnline} />
        <StatCard title="Total Revenue" value={stats.revenue} />
        <StatCard title="Shops on Platform" value={stats.shopCount} />
      </div>

      <div className="space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <IframeContainer title="User Activity" src={iframeSrcs.userActivity} />
          <IframeContainer title="Sales Overview" src={iframeSrcs.salesOverview} />
        </div>
        <IframeContainer
          title="Product Performance"
          src={iframeSrcs.productPerformance}
          height="600px"
        />
      </div>
    </div>
  );
}
