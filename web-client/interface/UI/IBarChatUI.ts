export interface IChartData {
  month: string;
  [key: string]: string | number; //dynamic keys
}

export interface IChartConfig {
  label: string;
  color: string;
}

export interface IChartConfigGroup {
  [key: string]: IChartConfig; //dynamic keys
}

export interface IBarChartComponentProps {
  title: string;
  description: string;
  data: IChartData[];
  config: IChartConfigGroup;
  footerText: string;
}
