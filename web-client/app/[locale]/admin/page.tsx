"use client";

import { useEffect, useState, useCallback } from "react";
import { API_BASE_URL, API_ROUTES } from "@/libraries/api";
import StatCard from "@/components/stat_card";
import IframeContainer from "@/components/iframe_container";
import Spinner from "@/components/spinner";
import { usePathname } from "next/navigation";
import { useRouter } from "next/navigation";
import { Button, Table, TableHeader, TableColumn, TableBody, TableRow, TableCell } from "@nextui-org/react";
import { Home } from "lucide-react";

interface ICategoryStats {
  category_id: string;
  category_name: string;
  number_of_products: number;
}

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
  const router = useRouter();
  const pathname = usePathname();
  const locale = pathname.split("/")[1];
  const [categoryStats, setCategoryStats] = useState<ICategoryStats[]>([]);

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

  const fetchCategoryStats = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}${API_ROUTES.GET_PRODUCT_CAT}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });
      
      if (!response.ok) throw new Error('Failed to fetch category statistics');
      const data = await response.json();
      setCategoryStats(data);
    } catch (error) {
      console.error('Error fetching category statistics:', error);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      await fetchNumber(API_ROUTES.USERS_NUMBER, "usersOnline");
      await fetchNumber(API_ROUTES.REVENUE_CURRENT, "revenue");
      await fetchNumber(API_ROUTES.SHOPS_NUMBER, "shopCount");
      await fetchCategoryStats();

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
  }, [fetchNumber, fetchChart]);

  if (isLoading) {
    return <Spinner />;
  }

  return (
    <div className="relative">
      <Button 
        onClick={() => router.push(`/${locale}`)}
        className="absolute top-4 right-4 bg-primary text-white"
        startContent={<Home size={20} />}
      >
        Home
      </Button>

      <h1 className="text-3xl font-bold mb-8">Admin Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <StatCard title="Users Online" value={stats.usersOnline} />
        <StatCard title="Total Revenue" value={stats.revenue} />
        <StatCard title="Shops on Platform" value={stats.shopCount} />
      </div>

      <div className="mb-8 p-6 bg-white rounded-lg shadow">
        <h2 className="text-2xl font-semibold mb-4">Category Statistics</h2>
        
        <Table aria-label="Category statistics table">
          <TableHeader>
            <TableColumn>CATEGORY NAME</TableColumn>
            <TableColumn>NUMBER OF PRODUCTS</TableColumn>
          </TableHeader>
          <TableBody>
            {categoryStats.map((category) => (
              <TableRow key={category.category_id}>
                <TableCell>{category.category_name}</TableCell>
                <TableCell>{category.number_of_products}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
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
  );
}
