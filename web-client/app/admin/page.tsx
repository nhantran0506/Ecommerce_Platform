"use client";

import { useEffect, useState } from "react";
import { API_BASE_URL, API_ROUTES } from "@/libraries/api";

export default function AdminPage() {
  const [iframeSrc, setIframeSrc] = useState<string | null>(null);
  const [selectedMonth, setSelectedMonth] = useState<string>(getCurrentMonth());

  function getCurrentMonth() {
    const now = new Date();
    return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
  }

  const fetchChart = async (timestamp: string) => {
    try {

      const response = await fetch(
        `${API_BASE_URL}${API_ROUTES.ADMIN_REVENUE}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify({ timestamp : timestamp }),
        }
      );

      console.log(JSON.stringify({ timestamp : timestamp }))
      if (!response.ok) {
        throw new Error("Failed to fetch chart");
      }

      const chartHtml = await response.text();
      const blob = new Blob([chartHtml], { type: "text/html" });
      const url = URL.createObjectURL(blob);

      setIframeSrc(url);
    } catch (error) {
      console.error("Error fetching chart:", error);
    }
  };

  useEffect(() => {
    fetchChart(getCurrentMonth());

    return () => {
      if (iframeSrc) {
        URL.revokeObjectURL(iframeSrc);
      }
    };
  }, []);

  const handleReload = () => {
    if (iframeSrc) {
      URL.revokeObjectURL(iframeSrc);
    }
    fetchChart(selectedMonth);
  };

  return (
    <div className="p-4">
      <div className="mb-4 flex items-center">
        <input
          type="month"
          value={selectedMonth}
          onChange={(e) => setSelectedMonth(e.target.value)}
          className="mr-2 p-2 border rounded"
        />
        <button
          onClick={handleReload}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Reload
        </button>
      </div>
      {iframeSrc ? (
        <iframe
          src={iframeSrc}
          style={{ width: "100%", height: "600px", border: "none" }}
          title="Revenue Chart"
        />
      ) : (
        <p>Loading chart...</p>
      )}
    </div>
  );
}
