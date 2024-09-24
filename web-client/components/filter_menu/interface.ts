import { ReactNode } from "react";

export interface IFilterMenuItem {
  title: string;
  content: ReactNode;
}

export interface ICheckBoxItem {
  name: string;
}

export interface IListCheckBox {
  listCheckBox: ICheckBoxItem[];
}
