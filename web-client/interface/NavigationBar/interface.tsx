import { ReactNode } from "react";

export interface IHomePageOption {
  name: string;
  link: string;
}

export interface IDropDownOption {
  key: string;
  prefix?: ReactNode;
  name: string;
  color?:
    | "danger"
    | "default"
    | "primary"
    | "secondary"
    | "success"
    | "warning"
    | undefined;
}
