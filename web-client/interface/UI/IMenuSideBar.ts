import { ReactNode } from "react";

export interface IMenuSideBar {
  parentEndPoint: string;
  listTabs: IMenuSideBarItem[];
}

export interface IMenuSideBarItem {
  prefix: ReactNode;
  name: string;
  endpoint: string;
}
