import { UserRoleEnum } from "@/state/enum";

export interface IReqLogin {
  user_name: string;
  password: string;
}

export interface IResLogin {
  token: string;
  type: string;
}

export interface IResGetUser {
  user_id: string;
  phone_number: string;
  dob: string;
  role: string;
  first_name: string;
  last_name: string;
  address: string;
  email: string;
}

export interface IReqUpdateUser {
  first_name: string;
  last_name: string;
  address: string;
  dob: string;
}
