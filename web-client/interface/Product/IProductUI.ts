import { ReactNode } from "react";

export interface IProductIconDataSection {
  prefix: ReactNode;
  data: string;
  subText?: string;
  isHightlight?: boolean;
}

export enum ImageSizeEnum {
  sm,
  lg,
}

export interface IProductDefaultImage {
  imgSize: ImageSizeEnum;
}
