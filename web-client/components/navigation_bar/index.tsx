"use client";

import React from "react";
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
} from "@nextui-org/react";
import { LogOut, Settings, ShoppingCart, User } from "react-feather";
import { usePathname, useRouter } from "next/navigation";
import { IHomePageOption } from "../../interface/NavigationBar/interface";
import { MenuEnum } from "./enum";

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
    name: "Settings",
    link: "#",
  },
  {
    name: "Log In",
    link: "/login",
  },
  {
    name: "Log Out",
    link: "#",
  },
];

export default function NavigationBar() {
  const router = useRouter();
  const pathname = usePathname();

  const handleNavigate = (key: string) => {
    switch (key) {
      case MenuEnum.UserProfile:
        router.push(MenuEnum.UserProfile);
        break;
      case MenuEnum.Settings:
        router.push(MenuEnum.Settings);
        break;
      case MenuEnum.Cart:
        router.push(MenuEnum.Cart);
        break;
      case MenuEnum.Logout:
        // Handle logout logic (e.g., clearing tokens) before navigating
        router.push(MenuEnum.Logout);
        break;
      default:
        break;
    }
  };

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

      <NavbarContent justify="end" className="gap-8">
        <NavbarItem>
          <ShoppingCart onClick={() => handleNavigate(MenuEnum.Cart)} />
        </NavbarItem>

        <NavbarItem>
          <Dropdown placement="bottom-end">
            <DropdownTrigger>
              <User />
            </DropdownTrigger>
            <DropdownMenu
              aria-label="Profile Actions"
              variant="flat"
              onAction={(key) => handleNavigate(key as string)}
            >
              <DropdownItem key={MenuEnum.UserProfile}>
                <div className="flex items-center gap-3">
                  <User />
                  <p>Profile</p>
                </div>
              </DropdownItem>
              <DropdownItem key={MenuEnum.Settings}>
                <div className="flex items-center gap-3">
                  <Settings />
                  <p>Settings</p>
                </div>
              </DropdownItem>
              <DropdownItem key={MenuEnum.Logout} color="danger">
                <div className="flex items-center gap-3">
                  <LogOut />
                  <p> Log Out</p>
                </div>
              </DropdownItem>
            </DropdownMenu>
          </Dropdown>
        </NavbarItem>
      </NavbarContent>

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
