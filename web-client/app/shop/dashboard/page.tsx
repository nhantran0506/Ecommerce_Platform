"use client";

import { BarChartComponent } from "@/components/dashboard/bar_chard";
import SectionHeader from "@/components/section_header";
import { IChartConfigGroup, IChartData } from "@/interface/UI/IBarChatUI";

// Default data for the chart
const chartData: IChartData[] = [
  { month: "January", desktop: 186, mobile: 80, laptop: 80 },
  { month: "February", desktop: 305, mobile: 200, laptop: 80 },
  { month: "March", desktop: 237, mobile: 120, laptop: 80 },
  { month: "April", desktop: 73, mobile: 190, laptop: 80 },
  { month: "May", desktop: 209, mobile: 130, laptop: 80 },
  { month: "June", desktop: 214, mobile: 140, laptop: 80 },
  { month: "July", desktop: 220, mobile: 144, laptop: 80 },
  { month: "August", desktop: 220, mobile: 144, laptop: 80 },
  { month: "September", desktop: 220, mobile: 144, laptop: 80 },
  { month: "October", desktop: 220, mobile: 144, laptop: 80 },
  { month: "November", desktop: 220, mobile: 144, laptop: 80 },
  { month: "December", desktop: 220, mobile: 144, laptop: 80 },
];

// Default configuration for the chart
const chartConfig: IChartConfigGroup = {
  desktop: {
    label: "Desktop",
    color: "hsl(var(--chart-0))",
  },
  mobile: {
    label: "Mobile",
    color: "hsl(var(--chart-1))",
  },
  laptop: {
    label: "Laptop",
    color: "hsl(var(--chart-2))",
  },
};

const ShopDashBoard = () => {
  return (
    <SectionHeader
      title={"Total sale 2024 "}
      content={
        <BarChartComponent
          title={"This is title"}
          description={"October 2024"}
          data={chartData}
          config={chartConfig}
          footerText={"Some little description"}
        />
      }
    />
  );
};

export default ShopDashBoard;
