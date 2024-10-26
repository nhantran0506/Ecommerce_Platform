"use client";

import { useEffect, useState, useCallback } from "react";
import { API_BASE_URL, API_ROUTES } from "@/libraries/api";
import StatCard from "@/components/stat_card";
import IframeContainer from "@/components/iframe_container";
import Spinner from "@/components/spinner";
import AdminSidebar from "@/components/admin_sidebar";

export default function AdminPage() {
  const [stats, setStats] = useState({
    usersOnline: "0",
    revenue: "$0",
    shopCount: "0",
  });

  const [iframeSrcs, setIframeSrcs] = useState<{
    orderStat: string;
    incomeStats: string;
    catStats: string;
  }>({
    orderStat: "",
    incomeStats: "",
    catStats: "",
  });

  const [isLoading, setIsLoading] = useState(true);

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
        const value = data["results"];
        if (value) {
          setStats((prevStats) => ({
            ...prevStats,
            [field]: String(value),
          }));
        }




        if (field === "revenue") {

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
      await fetchNumber(API_ROUTES.USERS_NUMBER, "usersOnline");
      await fetchNumber(API_ROUTES.REVENUE_CURRENT, "revenue");
      await fetchNumber(API_ROUTES.SHOPS_NUMBER, "shopCount");

      const orderStatsSrc = await fetchChart(API_ROUTES.ORDER_STATS);
      const incomeStatsSrc = await fetchChart(API_ROUTES.INCOME_STATS);
      const catStatsSrc = await fetchChart(API_ROUTES.CAT_STATS);

      setIframeSrcs({
        orderStat: orderStatsSrc,
        incomeStats: incomeStatsSrc,
        catStats: catStatsSrc,
      });

      setIsLoading(false);
    };

    fetchData();

    return () => {
      Object.values(iframeSrcs).forEach((src) => {
        if (src) URL.revokeObjectURL(src);
      });
    };
  }, []);

  if (isLoading) {
    return <Spinner />;
  }

  return (
    <div className="flex">
      <AdminSidebar />
      <div className="flex-1 p-8 ml-64">
        <h1 className="text-3xl font-bold mb-8">Admin Dashboard</h1>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <StatCard title="Users Online" value={stats.usersOnline} />
          <StatCard title="Total Revenue" value={stats.revenue} />
          <StatCard title="Shops on Platform" value={stats.shopCount} />
        </div>

        <div className="space-y-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <IframeContainer title="Orders Overview" src={iframeSrcs.orderStat} />
            <IframeContainer title="Income Overview" src={iframeSrcs.incomeStats} />
          </div>
          <IframeContainer
            title="Category Overview"
            src={iframeSrcs.catStats}
            height="600px"
          />
        </div>
      </div>
    </div>
  );
}
