import { ReactNode } from "react";

export interface IMenuSideBar {
  prefix: ReactNode;
  name: string;
  child: ReactNode;
}

export interface IProfileInput {
  type: string;
  label: string;
  placeholder: string;
}
