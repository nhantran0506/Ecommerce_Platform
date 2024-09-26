import { ReactNode } from "react";

export interface IProductIconDataSection {
  prefix: ReactNode;
  data: string;
  subText?: string;
  isHightlight?: boolean;
}
