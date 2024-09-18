import { ReactNode } from "react";

export interface IFilterMenu {
  prefix: ReactNode;
  listFilterOption: IOptionMenuFilter[];
}

export interface IOptionMenuFilter {
  key: string;
  label: string;
}
