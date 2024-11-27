interface IReqLogin {
  user_name: string;
  password: string;
}

interface IResLogin {
  token: string;
  type: string;
}
