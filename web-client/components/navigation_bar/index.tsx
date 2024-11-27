"use client";

import React, { useEffect, useState } from "react";
import {
  Navbar,
  NavbarBrand,
  NavbarMenuToggle,
  NavbarMenuItem,
  NavbarMenu,
  NavbarContent,
  NavbarItem,
  Link,
  Button,
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
  DropdownSection,
  Image,
} from "@nextui-org/react";
import { LogOut, ShoppingCart, User } from "react-feather";
import { usePathname, useRouter } from "next/navigation";
import { IDropDownOption, IHomePageOption } from "../../interface/UI/INavBar";
import { MenuEnum } from "./enum";
import { Moon, Sun } from "lucide-react";
import vietNamImg from "@/assets/vietnam.png";
import usImg from "@/assets/united-states-of-america.png";

const hideNavigationPaths = ["/admin"];

const pageNavigation: IHomePageOption[] = [
  {
    name: "Home",
    link: MenuEnum.Home,
  },
  {
    name: "Products",
    link: MenuEnum.Product,
  },
  {
    name: "Shop",
    link: MenuEnum.Shop,
  },
];

const pageMenu: IHomePageOption[] = [
  ...pageNavigation,
  {
    name: "Log In",
    link: "/login",
  },
  {
    name: "Log Out",
    link: "#",
  },
];

const userDropdownOption: IDropDownOption[] = [
  {
    key: MenuEnum.UserProfile,
    prefix: <User />,
    name: "Profile",
  },
  {
    key: MenuEnum.Logout,
    prefix: <LogOut />,
    name: "Log Out",
    color: "danger",
  },
];

export default function NavigationBar() {
  const router = useRouter();
  const pathname = usePathname();
  const [isDarkMode, setIsDarkMode] = useState<boolean>(false);
  const [isVietNamese, setIsVietNamese] = useState<boolean>(false);
  const [isLogin, setIsLogin] = useState<boolean>(false);

  const token = localStorage.getItem("token");

  useEffect(() => {
    if (token && token != "") setIsLogin(true);
  }, [token]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsLogin(false);

    router.push(MenuEnum.LogIn);
  };

  const handleNavigate = (key: string) => {
    switch (key) {
      case MenuEnum.UserProfile:
        router.push(MenuEnum.UserProfile);
        break;
      case MenuEnum.Cart:
        router.push(MenuEnum.Cart);
        break;
      case MenuEnum.Logout:
        handleLogout();
        break;
      case MenuEnum.LogIn:
        router.push(MenuEnum.LogIn);
        break;
      default:
        break;
    }
  };

  const handleSwitchTheme = () => {
    setIsDarkMode(!isDarkMode);

    // TODO: change theme
  };

  const handleSwitchLanguages = () => {
    setIsVietNamese(!isVietNamese);

    // TODO: change Languages
  };

  if (hideNavigationPaths.some((path) => pathname.startsWith(path))) {
    return null;
  }

  return (
    <Navbar disableAnimation isBordered>
      <NavbarContent className="sm:hidden" justify="start">
        <NavbarMenuToggle />
      </NavbarContent>

      <NavbarContent className="sm:hidden pr-3" justify="center">
        <NavbarBrand>
          <p className="font-bold text-inherit">LOGO</p>
        </NavbarBrand>
      </NavbarContent>

      <NavbarContent className="hidden sm:flex gap-8" justify="center">
        <NavbarBrand>
          <p className="font-bold text-inherit">LOGO</p>
        </NavbarBrand>
        {pageNavigation.map((item, index) => {
          return (
            <NavbarItem
              isActive={pathname == item.link ? true : false}
              key={index}
            >
              <Link color="foreground" href={item.link}>
                {item.name}
              </Link>
            </NavbarItem>
          );
        })}
      </NavbarContent>

      <NavbarContent justify="end" className="gap-4">
        <NavbarItem>
          <Button
            isIconOnly
            className="bg-transparent"
            onClick={() => handleSwitchLanguages()}
          >
            {isVietNamese ? (
              <Image
                src={vietNamImg.src}
                alt="vietnam-img"
                width={30}
                radius="none"
              />
            ) : (
              <Image src={usImg.src} alt="us-img" width={35} radius="none" />
            )}
          </Button>
        </NavbarItem>

        <NavbarItem>
          <Button
            isIconOnly
            className="bg-transparent"
            onClick={() => handleSwitchTheme()}
          >
            {isDarkMode ? <Moon /> : <Sun />}
          </Button>
        </NavbarItem>

        <NavbarItem>
          <Button isIconOnly className="bg-transparent">
            <ShoppingCart onClick={() => handleNavigate(MenuEnum.Cart)} />{" "}
          </Button>
        </NavbarItem>

        <NavbarItem>
          <Dropdown placement="bottom-end">
            <DropdownTrigger>
              <Button isIconOnly className="bg-transparent">
                <User />
              </Button>
            </DropdownTrigger>
            <DropdownMenu
              aria-label="Profile Actions"
              variant="flat"
              onAction={(key) => handleNavigate(key as string)}
            >
              <DropdownItem key="name">
                <p className="text-lg text-black font-bold">
                  {isLogin ? "Phuoc Truong" : "Welcome 👋"}
                </p>
              </DropdownItem>
              <DropdownSection>
                {isLogin ? (
                  userDropdownOption.map((item, index) => (
                    <DropdownItem key={item.key} color={item.color}>
                      <div className="flex items-center gap-3">
                        {item.prefix}
                        <p>{item.name}</p>
                      </div>
                    </DropdownItem>
                  ))
                ) : (
                  <DropdownItem onClick={() => handleNavigate(MenuEnum.LogIn)}>
                    Login
                  </DropdownItem>
                )}
              </DropdownSection>
            </DropdownMenu>
          </Dropdown>
        </NavbarItem>
      </NavbarContent>

      {/* responsive ui */}
      <NavbarMenu>
        {pageMenu.map((item, index) => (
          <NavbarMenuItem key={`${item}-${index}`}>
            <Link
              className="w-full"
              color={
                index === 2
                  ? "warning"
                  : index === pageMenu.length - 1
                  ? "danger"
                  : "foreground"
              }
              href={item.link}
              size="lg"
            >
              {item.name}
            </Link>
          </NavbarMenuItem>
        ))}
      </NavbarMenu>
    </Navbar>
  );
}
