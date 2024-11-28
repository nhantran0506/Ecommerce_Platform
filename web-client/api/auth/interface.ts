interface IReqLogin {
  user_name: string;
  password: string;
}

interface IResLogin {
  token: string;
  type: string;
}

interface IResGetUser {
  user_id: string;
  phone_number: string;
  dob: string;
  role: string;
  first_name: string;
  last_name: string;
  address: string;
  email: string;
}

interface IReqUpdateUser {
  first_name: string;
  last_name: string;
  address: string;
  dob: string;
}
